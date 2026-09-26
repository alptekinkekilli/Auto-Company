---
name: Analyst engine
slug: analyst-engine
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
sources_digest: 7f8e7d6a9e197732a06d93ee9f99e03a2a50ef0721c7d992f3621f154f72a6b3
links:
  - to: auto-loop-harness
    relation: uses
    description: Runs as a cycle engine within the loop.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The offline-testable analyst engine scripts/analyst/opportunity-analyst-jcode.sh, which runs jcode with provider-specific env vars (JCODE_ANTHROPIC_REASONING_EFFORT vs JCODE_OPENAI_REASONING_EFFORT) without leaking the other, dedupes done.session_id into logs/analyst-jcode-sessions.log, and writes the report header naming jcode/claude and claude-opus-5.

## Related

- uses [[auto-loop-harness]] — Runs as a cycle engine within the loop.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
