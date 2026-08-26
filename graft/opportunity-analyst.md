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
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: scripts/analyst/opportunity-analyst.sh
    hash: a0a766435a1f9e501b97cca96bb30314440de72fd569313488d3b80d5f9c55a5
  - path: scripts/analyst/promote_directive.py
    hash: 9c45147f1730fc30545b94a30428d54e0bd40f04506aa3db00614880ec93d677
sources_digest: 0e30aa01e58354844cc15ea6a1e05fcee433c04412f00d5b4955c540c51d2eaf
links:
  - to: auto-loop-daemon
    relation: part_of
    description: >-
      Analyst Codex sessions are budget-excluded by auto-loop.sh when their
      thread IDs parse cleanly.
  - to: directive-writer
    relation: uses
    description: >-
      Calls directive_writer.py for snapshot/restore and promotion of
      human-directive.md.
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

Independent 'second-brain' (APP-221) that invokes Codex or jcode with the autocompany-opportunity-director skill to analyze the Tender Track portfolio and produce a decision report plus candidate-registry update. Never auto-applies directives (snapshot/restore with hash check); preserves the registry's historical journal by only editing the live span via merge_registry.py; runs a deterministic promotion gate via promote_directive.py. Records thread IDs to session logs for budget exclusion, avoids passing large file contents as prompt args to prevent E2BIG, and treats opportunity-scan.md as historical input to be ignored. The jcode variant (2026-08-24 re-charter) retires the registry merge and directive promotion passes entirely, writing only analysis-directive.md in audit-only mode.

## Related

- part of [[auto-loop-daemon]] — Analyst Codex sessions are budget-excluded by auto-loop.sh when their thread IDs parse cleanly.
- uses [[directive-writer]] — Calls directive_writer.py for snapshot/restore and promotion of human-directive.md.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
