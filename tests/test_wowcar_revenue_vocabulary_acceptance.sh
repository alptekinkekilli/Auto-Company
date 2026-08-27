#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mode="${1:-}"
report="${2:-/tmp/wowcar-revenue-vocabulary-${mode:-invalid}.json}"

case "$mode" in
  unchanged|14-anchor) ;;
  *) echo "usage: $0 {unchanged|14-anchor} [absolute-report-path]" >&2; exit 2 ;;
esac

exec python3 "$repo_root/scripts/ops/wowcar-revenue-vocabulary-acceptance.py" \
  --mode "$mode" \
  --candidate "$repo_root/projects/wowcar/generator-source/kod" \
  --report "$report"
