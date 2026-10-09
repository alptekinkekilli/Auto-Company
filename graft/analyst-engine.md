---
name: Analyst Engine
slug: analyst-engine
type: system
sources:
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
sources_digest: 7ca211bb37041821ad7da0e305f3f7fce2c4347757a207495fc1148cbb89f6b0
links:
  - to: state-snapshot-probe
    relation: produces
    description: >-
      The auditor report hash (analysis-directive.md) is one of the five watched
      surfaces
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The opportunity-analyst-jcode.sh harness that runs a jcode analyst session, with provider-specific credential handling (Claude fails closed naming CLAUDE_CODE_OAUTH_TOKEN, OpenAI requires openai-auth.json), effort level riding the provider-specific env var without leaking the other, and done.session_id deduped into logs/analyst-jcode-sessions.log. The report header in memories/analysis-directive.md names jcode/claude and the model claude-opus-5.

## Related

- produces [[state-snapshot-probe]] — The auditor report hash (analysis-directive.md) is one of the five watched surfaces
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
