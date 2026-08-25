---
name: docker & host hygiene
slug: docker-host-hygiene
type: system
sources:
  - path: scripts/linux/noop-action.sh
    hash: 0f0aaa7c6c79e6c7844c7528a253084811b9a9b7277f557a1a60a8011347f4d9
  - path: scripts/linux/status-linux.sh
    hash: 1dc4a455fe8ffdd5e1696608d50d02311afd701906d80ee26d5708374d3947d8
  - path: scripts/ops/docker-prune-safe.sh
    hash: 7f22912e40c9235114d147f0fb3949880a970ed7104ffcee964c37b187a1cb1d
sources_digest: e3f55730d6ac1970da9988e83d072ad210149ea3a9d7a432ea79d466b690ac2e
links:
  - to: opportunity-analyst-orchestration
    relation: uses
    description: >-
      docker-prune-safe frequently prunes the analyst's pilot image, forcing the
      image-tag fallback.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Threshold-gated Docker disk-space guard that prunes images/containers at escalating tiers without ever touching volumes, and the container-adapted status/noop scripts. Failures are logged but tolerated.

## Related

- uses [[opportunity-analyst-orchestration]] — docker-prune-safe frequently prunes the analyst's pilot image, forcing the image-tag fallback.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
