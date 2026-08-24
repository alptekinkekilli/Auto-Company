---
name: Promotion Gate
slug: promotion-gate
type: concept
sources:
  - path: scripts/analyst/promote_directive.py
    hash: 9c45147f1730fc30545b94a30428d54e0bd40f04506aa3db00614880ec93d677
sources_digest: 529774ce95135d20964e1d42a6242cf44c9928383f17eac44213ac8385a782b9
links:
  - to: directive-writer
    relation: uses
    description: Writes the new directive through the same safe-write path.
  - to: opportunity-analyst
    relation: part_of
    description: Pass-3 of the analyst pipeline.
generator:
  version: 1
covers:
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

A deterministic, fail-closed gate (promote_directive.py) that decides whether the analyst's report may overwrite human-directive.md. Uses pure regex (never an LLM) to block on any risk-keyword hit, missing verdict keywords, or escalation language near the current Active Validation ID. Requires the live directive Status to be DONE, backs up the current file, writes a PENDING directive with audit metadata, and verifies via read-back. Deliberately over-includes risk terms to favor manual review over false negatives.

## Related

- uses [[directive-writer]] — Writes the new directive through the same safe-write path.
- part of [[opportunity-analyst]] — Pass-3 of the analyst pipeline.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
