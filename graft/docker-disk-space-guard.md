---
name: Docker disk-space guard
slug: docker-disk-space-guard
type: system
sources:
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: e24fe28b77d7c48047aeb9d7f3037b12372488dca9bbcb6208518f1e5efa731d
links:
  - to: opportunity-analyst-cron
    relation: depends_on
    description: >-
      Frequently prunes the analyst-jcode pilot image, forcing the cron's
      image-tag fallback.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Threshold-gated Docker disk-space guard preventing redeploy churn from exhausting the host's 38GB disk. Two escalation tiers: WARN (60%) runs only non-destructive builder/image prune (never touching containers so crash evidence survives); THRESH (70%) additionally prunes containers stopped >24h. Volumes are never touched per company-data constraint. Notifies by piping into the running app container (matched by name prefix z12a992) rather than dot-sourcing runtime.env because its values contain '|'.

## Related

- depends on [[opportunity-analyst-cron]] — Frequently prunes the analyst-jcode pilot image, forcing the cron's image-tag fallback.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
