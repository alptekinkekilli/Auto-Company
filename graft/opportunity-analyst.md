---
name: Opportunity Analyst
slug: opportunity-analyst
type: system
sources:
  - path: scripts/analyst/merge_registry.py
    hash: 55719338148054fff06780400062453a037e4bf10fe5817f04536b5c85ade7d1
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
  - path: scripts/analyst/promote_directive.py
    hash: 9c45147f1730fc30545b94a30428d54e0bd40f04506aa3db00614880ec93d677
sources_digest: 466cd5357bc86cd54e0c0bc2a6c4b3756df89d6f333d6ec3e184072f3ff7d3a8
links:
  - to: directive-writer
    relation: uses
    description: Uses directive_writer.py for safe restore of human-directive.md.
  - to: loop-driver
    relation: uses
    description: >-
      Shares the directive/consensus state files and the directive_writer
      guardrail with the loop.
generator:
  version: 1
covers:
  - symbol: identifier_fields
    kind: function
    at: 'scripts/analyst/merge_registry.py:L66-L76'
  - symbol: audit
    kind: function
    at: 'scripts/analyst/merge_registry.py:L79-L82'
  - symbol: blocked
    kind: function
    at: 'scripts/analyst/merge_registry.py:L85-L88'
  - symbol: extract_ids
    kind: function
    at: 'scripts/analyst/merge_registry.py:L91-L105'
  - symbol: extract_axes
    kind: function
    at: 'scripts/analyst/merge_registry.py:L108-L120'
  - symbol: table_rows
    kind: function
    at: 'scripts/analyst/merge_registry.py:L123-L131'
  - symbol: row_identity
    kind: function
    at: 'scripts/analyst/merge_registry.py:L134-L151'
  - symbol: sections
    kind: function
    at: 'scripts/analyst/merge_registry.py:L154-L163'
  - symbol: active_candidates
    kind: function
    at: 'scripts/analyst/merge_registry.py:L166-L186'
  - symbol: normalize_axis
    kind: function
    at: 'scripts/analyst/merge_registry.py:L189-L190'
  - symbol: resolve_span
    kind: function
    at: 'scripts/analyst/merge_registry.py:L193-L232'
  - symbol: _rewind_over_separators
    kind: function
    at: 'scripts/analyst/merge_registry.py:L235-L246'
  - symbol: split_registry
    kind: function
    at: 'scripts/analyst/merge_registry.py:L249-L272'
  - symbol: main
    kind: function
    at: 'scripts/analyst/merge_registry.py:L275-L428'
  - symbol: sha256
    kind: function
    at: 'scripts/analyst/promote_directive.py:L91-L92'
  - symbol: audit
    kind: function
    at: 'scripts/analyst/promote_directive.py:L95-L98'
  - symbol: blocked
    kind: function
    at: 'scripts/analyst/promote_directive.py:L101-L104'
  - symbol: notify
    kind: function
    at: 'scripts/analyst/promote_directive.py:L107-L113'
  - symbol: main
    kind: function
    at: 'scripts/analyst/promote_directive.py:L116-L225'
---
<!-- context:generated:start -->
## Summary

An independent 'second-brain' that invokes Codex or jcode with the autocompany-opportunity-director skill to audit the Tender Track portfolio and produce a decision report plus a candidate-registry update. Orchestrates three passes: write the report to analysis-directive.md (draft only, never auto-applied), splice a model-proposed replacement into the live span of candidate-registry.md via merge_registry.py, and run a deterministic promotion gate via promote_directive.py. Never auto-applies directives; snapshots/restores with hash checks and records session IDs for budget exclusion.

## Related

- uses [[directive-writer]] — Uses directive_writer.py for safe restore of human-directive.md.
- uses [[loop-driver]] — Shares the directive/consensus state files and the directive_writer guardrail with the loop.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
