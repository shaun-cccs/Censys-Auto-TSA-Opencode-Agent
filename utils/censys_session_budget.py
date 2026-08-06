#!/usr/bin/env python3
"""Inspect or reset the Censys session credit ledger.

Rate limits pace requests; this ledger caps *spend*. Every search page issued
through ``censys_query.censys_search_page`` and every aggregation issued through
``censys_aggregate.censys_aggregate`` charges the ledger before the request is
sent, and refuses once ``CENSYS_SESSION_CREDIT_CEILING`` would be exceeded.

    python utils/censys_session_budget.py status
    python utils/censys_session_budget.py reset

Every API action costs 1 credit on the enterprise plan - searches, aggregations
and regex (``advanced``) queries alike - and each additional page of 100 results
costs 1 more, so the ledger charges 1 per request. It is still only a local
estimate: the authoritative figure is the org balance delta reported by
``utils/censys_credits.py``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

from censys_query import (
    CREDIT_CEILING,
    CREDIT_LEDGER_FILE,
    read_credit_ledger,
)


def cmd_status() -> int:
    ledger = read_credit_ledger()
    spent = float(ledger.get("spent", 0.0))
    started = ledger.get("started_at")
    print(f"Ledger file   : {CREDIT_LEDGER_FILE}")
    print(f"Ceiling       : {CREDIT_CEILING:,.0f} credits" if CREDIT_CEILING > 0
          else "Ceiling       : (unset - no limit enforced)")
    print(f"Estimated spend: {spent:,.0f} credits")
    print(f"Requests       : {int(ledger.get('requests', 0)):,}")
    if CREDIT_CEILING > 0:
        print(f"Remaining      : {max(0.0, CREDIT_CEILING - spent):,.0f} credits")
    if started:
        print(f"Session age    : {int(time.time() - float(started))}s")
    return 0


def cmd_reset() -> int:
    try:
        CREDIT_LEDGER_FILE.write_text(
            json.dumps({"spent": 0.0, "requests": 0, "started_at": time.time()})
        )
    except OSError as exc:
        print(f"could not reset ledger: {exc}", file=sys.stderr)
        return 1
    print("Session credit ledger reset to 0.")
    return 0


def main(argv=None) -> int:
    # `tsa` exports CENSYS_TSA_PROG so usage strings name the command the user
    # actually typed ("tsa assess"), not this file, which is not on their PATH.
    parser = argparse.ArgumentParser(prog=os.environ.get("CENSYS_TSA_PROG"), description=__doc__)
    parser.add_argument("command", choices=("status", "reset"), nargs="?",
                        default="status")
    args = parser.parse_args(argv)
    return cmd_status() if args.command == "status" else cmd_reset()


if __name__ == "__main__":
    raise SystemExit(main())
