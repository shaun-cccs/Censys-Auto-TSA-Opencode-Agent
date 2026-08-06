#!/usr/bin/env bash
# Test runner.
#
#   tests/run.sh          fast suite: no opencode agent runs, no Censys, no network
#   tests/run.sh --live   also runs the live plugin-enforcement tests
#
# The live tests spawn real agents and cost model tokens. They cost zero Censys
# credits: every gated path throws before a Censys call executes, and the one
# command that would spend credits is deliberately blocked by the budget.

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
echo

python -m unittest discover -s tests -t . -p 'test_*.py' -v
