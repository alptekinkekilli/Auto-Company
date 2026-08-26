---
name: Docker disk guard
slug: docker-disk-guard
type: file
sources:
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: e24fe28b77d7c48047aeb9d7f3037b12372488dca9bbcb6208518f1e5efa731d
links:
  - to: opportunity-analyst-cron
    relation: uses
    description: >-
      Its pruning of the 'pilot' image is why the analyst cron needs a fallback
      image tag.
  - to: telegram-notification-channel
    relation: uses
    description: Pipes messages into the app container which invokes telegram-notify.sh.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Threshold-gated Docker disk-space guard preventing redeploy churn from exhausting the host's 38GB disk. Two escalation tiers: WARN runs only non-destructive builder/image pruning (never touching containers so crash evidence survives); THRESH additionally prunes stopped containers older than 24h. Volumes are never touched. Notifies via the running app container (avoiding dot-sourcing runtime.env because its values contain '|'), with a once-per-day WARN throttle.

## Related

- uses [[opportunity-analyst-cron]] — Its pruning of the 'pilot' image is why the analyst cron needs a fallback image tag.
- uses [[telegram-notification-channel]] — Pipes messages into the app container which invokes telegram-notify.sh.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
