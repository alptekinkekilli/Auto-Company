---
name: Opportunity Analyst
slug: opportunity-analyst
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 69985d473943f6d5adc94f51728ad97490391d0f517750ce54c9b785931bf5d6
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
sources_digest: 17f4e5386f1a4fbb0283498ca259cc80e6c56a994d2d7c376fa2f138fff7cba0
links:
  - to: directive-promotion-gate
    relation: uses
    description: >-
      Runs promote_directive.py to decide whether the report's proposed
      human-directive.md text may be applied.
  - to: directive-writer
    relation: uses
    description: Snapshot/restore guardrail for human-directive.md.
  - to: registry-merge
    relation: uses
    description: >-
      Extracts and splices the live span of candidate-registry.md with invariant
      checks.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Independent 'second-brain' (APP-221) that invokes a coding engine (Codex gpt-5.6-sol or jcode claude-opus-5) with the autocompany-opportunity-director skill to analyze the Tender Track portfolio and produce a decision report plus candidate-registry update. Runs three passes: write report draft (never auto-applied), splice the live span of candidate-registry.md via merge_registry.py with invariant checks, and a deterministic promotion gate via promote_directive.py. Never auto-applies directives; records session IDs to a budget-exclusion ledger.

## Related

- uses [[directive-promotion-gate]] — Runs promote_directive.py to decide whether the report's proposed human-directive.md text may be applied.
- uses [[directive-writer]] — Snapshot/restore guardrail for human-directive.md.
- uses [[registry-merge]] — Extracts and splices the live span of candidate-registry.md with invariant checks.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
