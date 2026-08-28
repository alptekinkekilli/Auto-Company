---
name: auto-loop.sh core loop
slug: auto-loop-sh-core-loop
type: system
sources:
  - path: scripts/core/auto-loop.sh
    hash: 332728052d5c8e3d8dbb64ca1d391062fc22c656cdb0a87d5e258b4f688d6103
sources_digest: e83a8e8032c2bc43a843b2b950aa2034327797a2081555c358b8a4ed9f508ec7
links:
  - to: mixed-harness-metadata-attribution
    relation: implements
  - to: prompt-assembly-contract
    relation: implements
  - to: prompt-transport-contract
    relation: implements
  - to: tier-ladder-budget-selection
    relation: implements
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The central orchestration script that runs engine cycles (claude, codex, jcode) in a mixed harness, assembling FULL_PROMPT, extracting per-cycle metadata, applying tier ladder and budget gates, and transporting prompts to engine CLIs. Many regression tests extract its function bodies via awk to test them in isolation.

## Related

- implements [[mixed-harness-metadata-attribution]]
- implements [[prompt-assembly-contract]]
- implements [[prompt-transport-contract]]
- implements [[tier-ladder-budget-selection]]
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
