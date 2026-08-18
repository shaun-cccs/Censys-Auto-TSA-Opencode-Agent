#!/usr/bin/env python3
"""Rate-limit profiles for a TSA session. Reached as `tsa limits`.

WHY THIS EXISTS
---------------
The shipped pacing was wrong in a way that cost hours. The rolling request
budget defaulted to **200 requests per hour**, while a real assessment issues
100-300 Censys actions - the saved specs in reports/ record runs of 215, 264 and
414 credits. So a normal run exhausted its own budget partway through, the
gateway raised, and the workflow prose told the agent to *wait it out*. One
report notes the shared budget "climbing from 1,150 to over 1,496 requests in the
rolling hour against a 200 default": the limiter was not protecting anything, it
was just stalling.

Pacing is also the wrong tool for the job it was doing. Spend is capped by the
credit ledger (see ``censys_query.CREDIT_CEILING``), which counts what actually
costs money. Pacing only decides how fast requests may leave, and Censys
enterprise tolerates far more than 20 per minute.

So pacing became a **session decision**: the interactive orchestrator asks once,
`tsa run --rate` sets it from the command line, and this module persists the
answer where every later subcommand - in every subagent, in every process - picks
it up.

    tsa limits            # what is in force, and where each number came from
    tsa limits none       # no pacing at all: fastest
    tsa limits fast       # bounded, but never in the way
    tsa limits standard   # the original conservative pacing
    tsa limits clear      # forget the choice, fall back to `fast`

WHY THE FALLBACK IS `fast`, NOT `standard`
------------------------------------------
Because forgetting to choose must not reintroduce the stall. `fast` still has a
per-minute cap and a rolling budget an order of magnitude above a whole run, so a
runaway loop is still bounded - but a legitimate run never waits. `standard` is
kept for anyone who wants the old behaviour and for reproducing an old run.

STANDARD LIBRARY ONLY, ON PURPOSE
---------------------------------
``censys_query`` imports this module to compute its defaults, so it must not
import the SDK or ``censys_query`` itself. That also means `tsa limits` works on a
machine with no dependencies installed.

PRECEDENCE
----------
An explicit CLI flag beats an environment variable, which beats the persisted
profile, which beats the fallback. The CLI wins for free: the flags' *defaults*
are the resolved values, so passing one overrides them.

SCOPE
-----
The profile is machine-global, like the request budget and the credit ledger it
governs. Two TSAs running side by side share it. That is a deliberate trade: a
bash command cannot see an opencode session id, and inventing a session key that
the tools cannot resolve would be worse than a documented shared default.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

#  Outside any workspace, next to the rate-state and credit ledgers, and reached
#  only through `tsa limits`. Agents must never open it by path: a path outside
#  the workspace trips opencode's external-directory permission, which inside a
#  subagent has no UI to answer it and hangs the run.
LIMITS_FILE = Path(
    os.environ.get(
        "CENSYS_TSA_LIMITS_FILE",
        Path.home() / ".censys_tsa_limits.json",
    )
)

#  min_interval    seconds between two requests from one process
#  max_per_minute  sliding 60s cap per process; 0 disables
#  budget_requests rolling cross-run request budget; 0 disables
#  budget_window   length of that rolling window, seconds
#  concurrency     requests in flight for the batching entrypoints
PROFILES: Dict[str, Dict[str, Any]] = {
    "none": {
        "min_interval": 0.0,
        "max_per_minute": 0,
        "budget_requests": 0,
        "budget_window": 3600.0,
        # Still a ceiling, not "unlimited": sockets and the Censys 429 handler
        # both have opinions, and a hundred parallel requests would find them.
        "concurrency": 12,
        "why": "no pacing; the credit ceiling is the only guard",
    },
    "fast": {
        "min_interval": 0.0,
        "max_per_minute": 120,
        "budget_requests": 5000,
        "budget_window": 3600.0,
        "concurrency": 8,
        "why": "bounded well above a full run, so it never stalls one",
    },
    "standard": {
        "min_interval": 1.0,
        "max_per_minute": 20,
        "budget_requests": 200,
        "budget_window": 3600.0,
        "concurrency": 1,
        "why": "the original conservative pacing; below what one run needs",
    },
}

FALLBACK_PROFILE = "fast"

SETTINGS = ("min_interval", "max_per_minute", "budget_requests", "budget_window", "concurrency")

#  Environment overrides, which sit between the profile and an explicit flag.
ENV_KEYS = {
    "min_interval": "CENSYS_MIN_INTERVAL",
    "max_per_minute": "CENSYS_MAX_PER_MINUTE",
    "budget_requests": "CENSYS_BUDGET_REQUESTS",
    "budget_window": "CENSYS_BUDGET_WINDOW",
    "concurrency": "CENSYS_CONCURRENCY",
}

CASTS = {
    "min_interval": float,
    "max_per_minute": int,
    "budget_requests": int,
    "budget_window": float,
    "concurrency": int,
}


def read_state() -> Dict[str, Any]:
    """The persisted choice, or an empty dict. Never raises."""
    try:
        data = json.loads(LIMITS_FILE.read_text())
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def write_state(profile: str, by: str = "") -> Dict[str, Any]:
    state = {"profile": profile, "set_at": time.time(), "by": by or "tsa limits"}
    LIMITS_FILE.parent.mkdir(parents=True, exist_ok=True)
    LIMITS_FILE.write_text(json.dumps(state))
    return state


def clear_state() -> None:
    try:
        LIMITS_FILE.unlink()
    except FileNotFoundError:
        pass


def profile_name() -> str:
    """Which profile is in force, ignoring environment overrides."""
    name = str(read_state().get("profile") or "")
    return name if name in PROFILES else FALLBACK_PROFILE


def resolve() -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Return ``(settings, provenance)`` - the numbers, and where each came from.

    Provenance is not decoration: "why is this run pacing itself" is the exact
    question that took hours to answer before this existed.
    """
    name = profile_name()
    settings = {key: PROFILES[name][key] for key in SETTINGS}
    source = "fallback" if not read_state() else "profile"
    provenance = {key: f"{source} ({name})" for key in SETTINGS}

    for key, env_key in ENV_KEYS.items():
        raw = os.environ.get(env_key)
        if raw is None or raw == "":
            continue
        try:
            settings[key] = CASTS[key](raw)
        except (TypeError, ValueError):
            continue
        provenance[key] = f"env {env_key}"
    return settings, provenance


def effective() -> Dict[str, Any]:
    """Just the numbers. What ``censys_query`` builds its defaults from."""
    return resolve()[0]


# ------------------------------------------------------------------- reporting


def format_status() -> str:
    settings, provenance = resolve()
    state = read_state()
    name = profile_name()
    lines = [
        f"Profile        : {name}"
        + ("" if state else f"   (nothing chosen - falling back to {FALLBACK_PROFILE})"),
        f"                 {PROFILES[name]['why']}",
        "",
        f"min interval   : {settings['min_interval']}s"
        + ("  (no wait between requests)" if not settings["min_interval"] else "")
        + f"   [{provenance['min_interval']}]",
        f"per-minute cap : "
        + ("off" if not settings["max_per_minute"] else str(settings["max_per_minute"]))
        + f"   [{provenance['max_per_minute']}]",
        f"request budget : "
        + (
            "off"
            if not settings["budget_requests"]
            else f"{settings['budget_requests']} per {int(settings['budget_window'])}s"
        )
        + f"   [{provenance['budget_requests']}]",
        f"concurrency    : {settings['concurrency']}   [{provenance['concurrency']}]",
        "",
        "Pacing is not a spend limit. Credits are capped separately - see "
        "`tsa budget`.",
    ]
    if state.get("set_at"):
        age = int(time.time() - float(state["set_at"]))
        lines.append(f"Chosen {age}s ago by {state.get('by', '?')}.")
    return "\n".join(lines)


def main(argv=None) -> int:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa limits"), not this file, which is not on their PATH.
    parser = argparse.ArgumentParser(
        prog=os.environ.get("CENSYS_TSA_PROG"),
        description="Choose how fast this machine may issue Censys requests.",
        epilog=(
            "none = no pacing (fastest; credits still capped) · "
            "fast = bounded but never in the way · "
            "standard = the original conservative pacing"
        ),
    )
    parser.add_argument(
        "action",
        nargs="?",
        default="show",
        choices=("show", "status", "clear", *PROFILES),
        help="A profile name to set, or show/clear",
    )
    parser.add_argument("--by", default="", help="Who chose it, recorded for provenance")
    parser.add_argument("-f", "--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    if args.action in PROFILES:
        try:
            write_state(args.action, args.by)
        except OSError as exc:
            print(f"could not persist the profile: {exc}", file=sys.stderr)
            return 1
    elif args.action == "clear":
        clear_state()

    if args.format == "json":
        settings, provenance = resolve()
        print(json.dumps(
            {"profile": profile_name(), "settings": settings, "provenance": provenance},
            indent=2,
        ))
    else:
        print(format_status())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
