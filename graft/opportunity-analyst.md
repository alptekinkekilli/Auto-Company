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
  - to: directive-writer
    relation: uses
    description: Uses directive_writer.py for safe restore of human-directive.md.
  - to: promotion-gate
    relation: uses
    description: >-
      Runs promote_directive.py to decide if the report's proposed directive
      text may be applied.
  - to: registry-merge
    relation: uses
    description: >-
      Uses merge_registry.py to extract and splice the live span of
      candidate-registry.md.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Independent 'second-brain' (APP-221) invoking Codex (gpt-5.6-sol, effort high) with the autocompany-opportunity-director skill to analyze the Tender Track portfolio. Three passes: write report draft (never auto-applied), extract live span of candidate-registry.md via merge_registry.py and splice back with invariant checks, and run a deterministic promotion gate. Never auto-applies directives; records Codex thread IDs for budget exclusion; treats opportunity-scan.md as historical input to ignore.

## Related

- uses [[directive-writer]] — Uses directive_writer.py for safe restore of human-directive.md.
- uses [[promotion-gate]] — Runs promote_directive.py to decide if the report's proposed directive text may be applied.
- uses [[registry-merge]] — Uses merge_registry.py to extract and splice the live span of candidate-registry.md.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
