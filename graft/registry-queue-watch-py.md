---
name: registry-queue-watch.py
slug: registry-queue-watch-py
type: system
sources:
  - path: scripts/ops/registry-queue-watch.py
    hash: 0ef6723d089c54ee8272050eb2776ce81af9de986e8f6dc15b065b7bbd913497
  - path: tests/test_registry_queue_watch.sh
    hash: 0c823a0b115d8fb57d7a64e25cb89f725943078e58504a22aa5306a416ac6668
sources_digest: 878ae52108871773ccdef2f91facc355fd5f130052a7558e98c93f83cf21f6fd
links: []
generator:
  version: 1
covers:
  - symbol: api_key
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L48-L58'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L61-L77'
  - symbol: main
    kind: function
    at: 'scripts/ops/registry-queue-watch.py:L80-L215'
---
<!-- context:generated:start -->
## Summary

Airtable-backed watcher (APP-277) that alerts only above threshold and respects cooldown via a state file, and distinguishes an empty bridge queue with many attribution-Held firms as a company gap rather than an operator gap. It also detects EKAP-only queues (a v1 blind spot) and clears state when the queue drains so the next backlog alerts immediately.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
