---
name: Opportunity Analyst (codex)
slug: opportunity-analyst-codex
type: system
sources:
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
sources_digest: da007f9034018dbd0503170144e8be4cae497ce9a604927f47722d34c5692a01
links:
  - to: directive-writer
    relation: uses
    description: Safe restore of human-directive.md.
  - to: promotion-gate
    relation: uses
    description: >-
      Pass 3 runs promote_directive.py to decide if the proposed directive may
      be applied.
  - to: registry-merge
    relation: uses
    description: Pass 2 extracts and splices the live span via merge_registry.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Independent 'second-brain' (APP-221) invoking OpenAI Codex with the autocompany-opportunity-director skill to analyze the Tender Track portfolio. Three passes: write report to analysis-directive.md (draft only, never auto-applied), extract the live span of candidate-registry.md via merge_registry.py and splice back a model-proposed replacement with invariant checks, and run a deterministic promotion gate via promote_directive.py. Never auto-applies directives (snapshot/restore with hash check), avoids E2BIG by not passing large files as prompt args, preserves the registry's historical journal by only editing the live span, and records Codex thread IDs for budget exclusion.

## Related

- uses [[directive-writer]] — Safe restore of human-directive.md.
- uses [[promotion-gate]] — Pass 3 runs promote_directive.py to decide if the proposed directive may be applied.
- uses [[registry-merge]] — Pass 2 extracts and splices the live span via merge_registry.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
