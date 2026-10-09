---
name: Infrastructure & disk hygiene
slug: infrastructure-disk-hygiene
type: system
sources:
  - path: scripts/graft-auto-refresh.py
    hash: 678e4a269c718dc9043afa096157f5d835cb3099883d31954de70ff10a4bfe33
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: 87308da8f3f12a81d7f73588a9b560c95ed87f2442550b00dae0c3b45230ac85
links:
  - to: sentry-heartbeat-crash-loop-detection
    relation: uses
    description: >-
      opportunity-analyst-cron resolves the image tag with fallback because
      docker-prune-safe frequently prunes the pilot image.
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

Host-level guards for the container deployment. docker-prune-safe.sh is a threshold-gated disk guard (WARN 60% non-destructive builder/image prune; THRESH 70% additionally prunes stopped containers older than 24h, never volumes), notifying by piping into the running container to read runtime.env rather than dot-sourcing it (values contain |). graft-auto-refresh.py is a SessionStart hook that triggers a paid deep graft build only when git history shows cards genuinely stale (double threshold: commits-behind and age), fail-open and non-blocking, with the Together API key never touching this script.

## Related

- uses [[sentry-heartbeat-crash-loop-detection]] — opportunity-analyst-cron resolves the image tag with fallback because docker-prune-safe frequently prunes the pilot image.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
