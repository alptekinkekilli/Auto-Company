---
name: Opportunity Analyst (jcode)
slug: opportunity-analyst-jcode
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
sources_digest: 7f8e7d6a9e197732a06d93ee9f99e03a2a50ef0721c7d992f3621f154f72a6b3
links:
  - to: directive-writer
    relation: uses
    description: Uses restore_directive guardrail via directive_writer.py.
  - to: jcode-mcp-config
    relation: uses
    description: References scripts/core/jcode-mcp-config.py for MCP config generation.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Production opportunity-analyst runner (jcode variant) that replaced the legacy codex path since the 2026-07-31 cutover. Invokes jcode (claude-opus-5, effort high) with a by-reference prompt to audit Wowcar 2.0 against human-directive.md, consensus.md, and operator-decisions.md. Includes a 126KB argv prompt-size guard against E2BIG, preflight against 'jcode model list' to avoid silent model substitution, provider-shaped auth (wrapping bare sk-ant-oat tokens in a claudeAiOauth envelope), and a 2026-08-24 re-charter that retires registry merge and directive promotion — the analyst now writes only analysis-directive.md in audit-only mode.

## Related

- uses [[directive-writer]] — Uses restore_directive guardrail via directive_writer.py.
- uses [[jcode-mcp-config]] — References scripts/core/jcode-mcp-config.py for MCP config generation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
