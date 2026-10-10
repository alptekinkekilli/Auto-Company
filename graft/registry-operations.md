---
name: registry operations
slug: registry-operations
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

Registry tooling: registry-archive.py archives stale dated sections while preserving a protected live span (from ## Selected through end of ## Exhausted patterns / lessons), moves frozen-pattern sections verbatim into a monthly archive, inserts pointer lines, idempotent, --check stays silent when nothing archivable; registry-queue-watch.py (APP-277) watches Airtable for pending registry requests, never cries wolf (fires only above threshold, respects cooldown), distinguishes empty bridge queue with many attribution-Held firms as a company gap not operator gap, detects EKAP-only queue (a v1 blind spot), persists cooldown via state file.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
