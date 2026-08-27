---
name: Opportunity Analyst
slug: opportunity-analyst
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
sources_digest: 4e45cb5db9a6fde1b9f645caeb93944c5fc63995f332b8bd5a848d8a702b1cf8
links:
  - to: directive-writer
    relation: uses
    description: Safe restore of human-directive.md via snapshot/restore with hash check.
  - to: promotion-gate
    relation: uses
    description: >-
      Pass 3 runs promote_directive.py to decide if the report's proposed
      human-directive.md text may be applied.
  - to: registry-merge
    relation: uses
    description: >-
      Pass 2 extracts the live span of candidate-registry.md via
      merge_registry.py and splices back the model's replacement.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Independent 'second-brain' (APP-221) that invokes an AI model (Codex gpt-5.6-sol or jcode claude-opus-5) with the autocompany-opportunity-director skill to analyze the Tender Track portfolio and produce a decision report plus candidate-registry update. Three passes: writes report to analysis-directive.md (draft only, never auto-applied), extracts the live span of candidate-registry.md via merge_registry.py and splices back a model-proposed replacement with invariant checks, and runs a deterministic promotion gate via promote_directive.py. Never auto-applies directives (snapshot/restore with hash check); avoids passing large file contents as prompt args (E2BIG); preserves the registry's historical journal by only editing the live span; records thread IDs to analyst-codex-sessions.log for budget exclusion. The 2026-08-24 re-charter retires the registry merge and directive promotion passes entirely — the analyst now writes only analysis-directive.md in audit-only mode, with the Tender Track frozen as historical state.

## Related

- uses [[directive-writer]] — Safe restore of human-directive.md via snapshot/restore with hash check.
- uses [[promotion-gate]] — Pass 3 runs promote_directive.py to decide if the report's proposed human-directive.md text may be applied.
- uses [[registry-merge]] — Pass 2 extracts the live span of candidate-registry.md via merge_registry.py and splices back the model's replacement.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
