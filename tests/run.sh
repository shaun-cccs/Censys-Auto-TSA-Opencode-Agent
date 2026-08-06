#!/usr/bin/env bash
# Test runner.
#
#   tests/run.sh          fast suite: no opencode agent runs, no Censys, no network
#   tests/run.sh --live   also runs the live plugin-enforcement tests
#
# The live tests spawn real agents and cost model tokens. They cost zero Censys
# credits: every gated path throws before a Censys call executes, and the one
# command that would spend credits is deliberately blocked by the budget.
#
# Interpreter selection matters here. There is no `python` on many machines -
# this kit exists partly because of that - so the runner prefers uv, which gives
# the suite the same locked environment the agents get and lets
# tests/test_censys_credits.py import the utils instead of skipping. Falling back
# to python3 keeps the static checks runnable with nothing installed at all.

set -euo pipefail
cd "$(dirname "$0")/.."

if [[ "${1:-}" == "--live" ]]; then
  echo "==> full suite (including live agent runs)"
  echo "    these spawn real agents and take several minutes"
  export TSA_LIVE_TESTS=1
else
  echo "==> fast suite (static checks only)"
  echo "    run with --live to also exercise plugin enforcement against real agents"
fi

find_uv() {
  if [[ -n "${CENSYS_TSA_UV:-}" ]]; then echo "$CENSYS_TSA_UV"; return 0; fi
  if command -v uv >/dev/null 2>&1; then command -v uv; return 0; fi
  for candidate in "$HOME/.local/bin/uv" "$HOME/.cargo/bin/uv"; do
    [[ -x "$candidate" ]] && { echo "$candidate"; return 0; }
  done
  return 1
}

if uv=$(find_uv); then
  echo "    interpreter: $uv run (locked environment)"
  echo
  exec "$uv" run --quiet --group dev python -m unittest discover -s tests -t . -p 'test_*.py' -v
fi

for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1; then
    echo "    interpreter: $candidate (no uv; SDK-dependent tests will skip)"
    echo
    exec "$candidate" -m unittest discover -s tests -t . -p 'test_*.py' -v
  fi
done

echo "no uv and no python3 on PATH" >&2
exit 127
