---
name: Docker disk guard
slug: docker-disk-guard
type: system
sources:
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: e24fe28b77d7c48047aeb9d7f3037b12372488dca9bbcb6208518f1e5efa731d
links:
  - to: telegram-notification
    relation: uses
    description: Pipes alerts into the app container to invoke telegram-notify.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Threshold-gated Docker disk-space guard preventing redeploy churn from exhausting the host's 38GB disk. Two escalation tiers: at WARN (60%) only non-destructive builder/image pruning (never touching containers so crash evidence survives); at THRESH (70%) additionally prunes containers stopped >24h. Volumes are never touched. Notifies by piping into the running app container rather than dot-sourcing the env file, whose values contain '|'.

## Related

- uses [[telegram-notification]] — Pipes alerts into the app container to invoke telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
