---
name: Opportunity Analyst (jcode)
slug: opportunity-analyst-jcode
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
sources_digest: 7f8e7d6a9e197732a06d93ee9f99e03a2a50ef0721c7d992f3621f154f72a6b3
links:
  - to: auto-loop
    relation: part_of
    description: Runs inside the company container; sessions logged for budget exclusion.
  - to: directive-writer
    relation: uses
    description: restore_directive guardrail.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Production opportunity-analyst runner (jcode variant) driving an AI audit of the Wowcar 2.0 program, replacing the legacy codex path since 2026-07-31. Invokes jcode (claude-opus-5, effort high) with a by-reference prompt; the model reads the wowcar-program-auditor SKILL.md and audits source docs against human-directive.md, consensus.md, operator-decisions.md, outputting a report without writing files. Preflights against 'jcode model list' to avoid silent model substitution, wraps bare sk-ant-oat tokens in a claudeAiOauth envelope, persists raw ndjson streams for cost calibration, and runs a non-fatal deterministic cost audit. Since 2026-08-24 re-charter, the registry merge and directive promotion passes are retired — the analyst writes only analysis-directive.md in audit-only mode.

## Related

- part of [[auto-loop]] — Runs inside the company container; sessions logged for budget exclusion.
- uses [[directive-writer]] — restore_directive guardrail.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
