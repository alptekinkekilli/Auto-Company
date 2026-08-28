---
name: docker-prune-safe
slug: docker-prune-safe
type: file
sources:
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: e24fe28b77d7c48047aeb9d7f3037b12372488dca9bbcb6208518f1e5efa731d
links:
  - to: telegram-notify
    relation: uses
    description: Pipes alert into the container which invokes telegram-notify.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Threshold-gated Docker disk-space guard preventing redeploy churn from exhausting 38GB host disk. WARN (60%): non-destructive builder/image prune only, never containers so crash evidence survives. THRESH (70%): additionally container prune --filter until=24h. Volumes never touched. Notifies by piping into running container (avoids dot-sourcing env file whose values contain |).

## Related

- uses [[telegram-notify]] — Pipes alert into the container which invokes telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
