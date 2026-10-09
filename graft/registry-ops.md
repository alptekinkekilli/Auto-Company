---
name: registry ops
slug: registry-ops
type: system
sources:
  - path: tests/test_registry_archive.sh
    hash: 4ca1be679dfb4867f1e05625b59c587e0a40e525f53c35404d535f93017e5c76
  - path: tests/test_registry_queue_watch.sh
    hash: 0c823a0b115d8fb57d7a64e25cb89f725943078e58504a22aa5306a416ac6668
sources_digest: f9962eef09d44a692d03d2d45eb468ea161e8eeb9b8bbffb1593f5928b172fdd
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

scripts/ops/registry-archive.py archives stale dated sections from a candidate registry markdown while preserving a protected live span (## Selected through ## Exhausted patterns / lessons) byte-identical, with dry-run/apply/check modes and idempotence. registry-queue-watch.py (APP-277) fires only above threshold with cooldown and distinguishes an empty bridge queue with attribution-Held firms as a company gap, not an operator gap, persisting state in .registry-queue-state.json.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
