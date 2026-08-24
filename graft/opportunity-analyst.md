---
name: Opportunity Analyst
slug: opportunity-analyst
type: system
sources:
  - path: >-
      scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
    hash: 79198378c25b2ff21cf5e4e2eda13f55c29ac806bd7f9d2bb0cba11a6268c447
  - path: scripts/analyst/merge_registry.py
    hash: 55719338148054fff06780400062453a037e4bf10fe5817f04536b5c85ade7d1
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 69985d473943f6d5adc94f51728ad97490391d0f517750ce54c9b785931bf5d6
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
  - path: scripts/analyst/promote_directive.py
    hash: 9c45147f1730fc30545b94a30428d54e0bd40f04506aa3db00614880ec93d677
sources_digest: c010151f753a62a451cf1c77b03eebce7e2458b48fd5ab21542c2ab59250be2a
links:
  - to: directive-writer
    relation: uses
    description: Uses directive_writer.py for safe snapshot/restore of human-directive.md.
  - to: promotion-gate
    relation: implements
    description: >-
      promote_directive.py is the deterministic fail-closed gate deciding
      whether the report may overwrite human-directive.md.
  - to: registry-merge-invariants
    relation: implements
    description: >-
      merge_registry.py enforces the live-span-only edit and candidate-identity
      invariants.
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

An independent 'second-brain' (APP-221) that invokes Codex or jcode with the autocompany-opportunity-director skill to analyze the Tender Track portfolio and produce a decision report plus a candidate-registry update. Runs three passes: writes a draft report (never auto-applied), extracts and splices only the live span of candidate-registry.md via merge_registry.py with invariant checks, and runs a deterministic promotion gate (promote_directive.py) before any directive text may be applied. Never auto-applies directives; records session IDs to a budget-exclusion ledger.

## Related

- uses [[directive-writer]] — Uses directive_writer.py for safe snapshot/restore of human-directive.md.
- implements [[promotion-gate]] — promote_directive.py is the deterministic fail-closed gate deciding whether the report may overwrite human-directive.md.
- implements [[registry-merge-invariants]] — merge_registry.py enforces the live-span-only edit and candidate-identity invariants.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
