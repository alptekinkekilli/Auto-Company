---
name: linux-runtime-scripts
slug: linux-runtime-scripts
type: system
sources:
  - path: scripts/linux/noop-action.sh
    hash: 0f0aaa7c6c79e6c7844c7528a253084811b9a9b7277f557a1a60a8011347f4d9
  - path: scripts/linux/status-linux.sh
    hash: 1dc4a455fe8ffdd5e1696608d50d02311afd701906d80ee26d5708374d3947d8
sources_digest: 22b579ab93665c664ddc3c622002ac6e6be26b450840f6e539abdab27d109689
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Container-mode lifecycle and status scripts. noop-action.sh is a placeholder for Start/Stop controls because Coolify manages the loop lifecycle (prevents false failures/invalid launchd commands). status-linux.sh emits the === Section === Key=Value format parse_macos_status_output expects, marking sleep guard not_applicable and assuming Coolify restart policy.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
