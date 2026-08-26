---
name: Promotion Gate
slug: promotion-gate
type: file
sources:
  - path: scripts/analyst/promote_directive.py
    hash: 9c45147f1730fc30545b94a30428d54e0bd40f04506aa3db00614880ec93d677
sources_digest: 529774ce95135d20964e1d42a6242cf44c9928383f17eac44213ac8385a782b9
links:
  - to: directive-writer
    relation: uses
    description: Writes the promoted directive through the sole writer.
  - to: opportunity-analyst
    relation: part_of
    description: PASS-3 promotion gate of the codex analyst variant.
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

Deterministic, fail-closed gate deciding whether the analyst's report may overwrite human-directive.md. Pure regex (never LLM) blocks on risk-keyword hits, missing verdict keywords, or escalation language near the current Active Validation ID. Requires live directive Status DONE; backs up, writes new directive with PENDING status, verifies via read-back/diff, logs and notifies. Always exits 0 printing PROMOTED or BLOCKED. Over-includes risk terms to favor manual review; no blanket NO-GO auto-promotion, no partial application.

## Related

- uses [[directive-writer]] — Writes the promoted directive through the sole writer.
- part of [[opportunity-analyst]] — PASS-3 promotion gate of the codex analyst variant.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
