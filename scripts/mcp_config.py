#!/usr/bin/env python3
"""Add, remove or check the Censys Platform MCP server in opencode's config.

Called by ``install.sh --mcp``. Standard library only, so it runs before the
kit's virtualenv exists.

The server authenticates with HTTP headers that reference the same two
environment variables the rest of the kit uses. The config file holds the
``{env:...}`` placeholders, never the values; opencode substitutes them when
it connects.

    mcp_config.py add    --config-dir DIR --major 1|2 [--dry-run]
    mcp_config.py remove --config-dir DIR --major 1|2 [--dry-run]
    mcp_config.py status --config-dir DIR --major 1|2

Exit codes: 0 done (or already in the wanted state), 1 not configured
(``status`` only), 2 the config cannot be edited safely - a printed snippet
says what to add by hand.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from pathlib import Path

NAME = "censys-platform"
URL = "https://mcp.platform.censys.io/platform/mcp/"
HEADERS = {
    "Authorization": "Bearer {env:CENSYS_PERSONAL_ACCESS_TOKEN}",
    "X-Organization-ID": "{env:CENSYS_ORG_ID}",
}


def server_entry() -> dict:
    """The server definition. Same shape on OpenCode 1 and 2."""
    return {"type": "remote", "url": URL, "headers": dict(HEADERS)}


def servers_of(config: dict, major: int) -> dict:
    """The dict that holds named servers: ``mcp.servers`` on V2, ``mcp`` on V1."""
    mcp = config.setdefault("mcp", {})
    if major >= 2:
        return mcp.setdefault("servers", {})
    return mcp


def is_ours(entry: object) -> bool:
    return isinstance(entry, dict) and entry.get("url") == URL


def snippet(major: int) -> str:
    body = {NAME: server_entry()}
    wrapped = {"mcp": {"servers": body}} if major >= 2 else {"mcp": body}
    return json.dumps(wrapped, indent=2)


def load(config_dir: Path) -> tuple[Path, dict] | None:
    """The global config as a dict, or None when it cannot be edited safely."""
    if (config_dir / "opencode.jsonc").exists():
        return None  # comments would be lost by a JSON round trip
    path = config_dir / "opencode.json"
    if not path.exists():
        return path, {"$schema": "https://opencode.ai/config.json"}
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        return None
    return (path, data) if isinstance(data, dict) else None


def save(path: Path, data: dict, dry_run: bool) -> None:
    if dry_run:
        print(f"  would: update {path}")
        return
    if path.exists():
        backup = path.with_name(f"{path.name}.{time.strftime('%Y%m%dT%H%M%S')}.before-censys-mcp")
        shutil.copy2(path, backup)
        print(f"  ok    backup {backup}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("action", choices=["add", "remove", "status"])
    p.add_argument("--config-dir", required=True, type=Path)
    p.add_argument("--major", type=int, choices=[1, 2], required=True)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    loaded = load(args.config_dir)
    if loaded is None:
        if args.action == "status":
            print(f"  WARN  cannot read {args.config_dir}/opencode.json(c) to check the MCP server")
            return 1
        print(f"  WARN  {args.config_dir}/opencode.json(c) has comments or is not plain JSON;")
        print("        not editing it. Add this by hand:\n")
        print(snippet(args.major))
        return 2
    path, config = loaded
    servers = servers_of(config, args.major)
    current = servers.get(NAME)

    if args.action == "status":
        if is_ours(current):
            print(f"  ok    MCP server {NAME} is configured")
            return 0
        print(f"  note  MCP server {NAME} is not configured (install.sh --mcp adds it)")
        return 1

    if args.action == "add":
        if is_ours(current):
            print(f"  ok    MCP server {NAME} already configured in {path}")
            return 0
        if current is not None:
            print(f"  WARN  {path} already has a different server named {NAME}; left alone")
            return 2
        servers[NAME] = server_entry()
        save(path, config, args.dry_run)
        print(f"  ok    MCP server {NAME} -> {URL}")
        return 0

    # remove
    if not is_ours(current):
        print(f"  absent MCP server {NAME}")
        return 0
    del servers[NAME]
    save(path, config, args.dry_run)
    print(f"  ok    removed MCP server {NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
