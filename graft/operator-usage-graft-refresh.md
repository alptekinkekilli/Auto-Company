---
name: Operator Usage & Graft Refresh
slug: operator-usage-graft-refresh
type: system
sources:
  - path: scripts/graft-auto-refresh.py
    hash: 678e4a269c718dc9043afa096157f5d835cb3099883d31954de70ff10a4bfe33
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
sources_digest: f75ddc6fdc889f2c6a367020d9e777180a51257202a130c86392313cb2755798
links:
  - to: cost-budget-ledger-adapters
    relation: uses
    description: >-
      operator-usage-report.sh's spend figure feeds the 14-day calibration
      report's operator-impact section.
generator:
  version: 1
covers:
  - symbol: _repo_root
    kind: function
    at: 'scripts/graft-auto-refresh.py:L42-L54'
  - symbol: _git
    kind: function
    at: 'scripts/graft-auto-refresh.py:L57-L68'
  - symbol: _lock_alive
    kind: function
    at: 'scripts/graft-auto-refresh.py:L71-L81'
  - symbol: _emit
    kind: function
    at: 'scripts/graft-auto-refresh.py:L84-L94'
  - symbol: main
    kind: function
    at: 'scripts/graft-auto-refresh.py:L97-L187'
  - symbol: status
    kind: function
    at: 'scripts/graft-auto-refresh.py:L122-L132'
  - symbol: fmt
    kind: function
    at: 'scripts/graft-auto-refresh.py:L134-L137'
---
<!-- context:generated:start -->
## Summary

Operator-machine and SessionStart hooks. operator-usage-report.sh pushes ccusage spend into the container via ssh/docker exec, failing silently so a stopped reporter degrades gracefully (mtime is the freshness signal). graft-auto-refresh.py triggers a paid deep graft build only when git history shows cards are genuinely stale (double threshold), fail-open and non-blocking, with the Together API key never touching this script.

## Related

- uses [[cost-budget-ledger-adapters]] — operator-usage-report.sh's spend figure feeds the 14-day calibration report's operator-impact section.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
