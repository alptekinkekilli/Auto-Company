---
name: Operator usage reporter
slug: operator-usage-reporter
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

Runs on the operator's machine to push current Claude usage into the container for loop calibration. Every failure path exits silently, leaving the file stale so the loop treats the operator as idle; the file's mtime is the freshness signal, so a stopped reporter degrades gracefully. The payload's blockStart anchors both 5-hour gates (per APP-263, the dynamic reserve cap is retired).
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
