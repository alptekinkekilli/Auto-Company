---
name: Opportunity Analyst
slug: opportunity-analyst
type: system
sources:
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
sources_digest: da007f9034018dbd0503170144e8be4cae497ce9a604927f47722d34c5692a01
links:
  - to: directive-writer
    relation: uses
    description: Uses directive_writer.py for safe restore of human-directive.md.
  - to: promotion-gate
    relation: uses
    description: >-
      Pass 3 runs promote_directive.py to decide whether the proposed
      human-directive.md text may be applied.
  - to: registry-merge
    relation: uses
    description: >-
      Pass 2 uses merge_registry.py to splice the live span of
      candidate-registry.md.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Independent 'second-brain' (APP-221) that invokes OpenAI Codex with the autocompany-opportunity-director skill to analyze the Tender Track portfolio. Orchestrates three passes: writes a draft report (never auto-applied), extracts the live span of candidate-registry.md via merge_registry.py and splices back a model-proposed replacement with invariant checks, and runs a deterministic promotion gate. Never auto-applies directives; records Codex thread IDs for budget exclusion; runs in danger-full-access sandbox mode.

## Related

- uses [[directive-writer]] — Uses directive_writer.py for safe restore of human-directive.md.
- uses [[promotion-gate]] — Pass 3 runs promote_directive.py to decide whether the proposed human-directive.md text may be applied.
- uses [[registry-merge]] — Pass 2 uses merge_registry.py to splice the live span of candidate-registry.md.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
