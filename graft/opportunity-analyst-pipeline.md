---
name: Opportunity analyst pipeline
slug: opportunity-analyst-pipeline
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: efc35f40b38b1b6430f80ca300088d4d14adbe07a6333a7a6bef744ced9eb5d1
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
sources_digest: 881c0d2223de3a50b3cf13b878fa98af59cd376ccddb3141459586f3af286ba1
links:
  - to: directive-writer
    relation: uses
    description: Snapshots/restores human-directive.md through directive_writer.py.
  - to: promotion-gate
    relation: uses
    description: Pass 3 applies the promotion gate via promote_directive.py.
  - to: registry-merge-tool
    relation: uses
    description: >-
      Pass 2 splices the live span of candidate-registry.md via
      merge_registry.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Independent second-brain that analyzes the Tender Track portfolio and produces a decision report plus candidate-registry update. Three passes: report draft (never auto-applied), registry live-span merge with invariant checks, and deterministic promotion gate.

## Related

- uses [[directive-writer]] — Snapshots/restores human-directive.md through directive_writer.py.
- uses [[promotion-gate]] — Pass 3 applies the promotion gate via promote_directive.py.
- uses [[registry-merge-tool]] — Pass 2 splices the live span of candidate-registry.md via merge_registry.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
