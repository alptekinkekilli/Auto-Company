---
name: operator-usage-report
slug: operator-usage-report
type: file
sources:
  - path: scripts/ops/operator-usage-report.sh
    hash: c469a1b0ab7be7c2c839b0ba0cf5a73d755ffd7f6e3d9891f924e61f1428eb4b
sources_digest: 0af75ce719ac85f974a4e4e7623396c84a6103f8d1b5951c4266ce14366245b4
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Runs on operator's machine to push current Claude usage into container for calibration. Invokes ccusage blocks --active, formats JSON, writes via ssh+docker exec to /app/logs/operator-usage.json. Every failure path exits silently leaving file stale so loop treats operator as idle. mtime is freshness signal. blockStart anchors 5-hour gates (dynamic reserve cap retired per APP-263).
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
