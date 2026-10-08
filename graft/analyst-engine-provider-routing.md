---
name: Analyst engine provider routing
slug: analyst-engine-provider-routing
type: system
sources:
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
sources_digest: 7ca211bb37041821ad7da0e305f3f7fce2c4347757a207495fc1148cbb89f6b0
links:
  - to: state-snapshot-delta-probing
    relation: produces
    description: >-
      The analyst report (analysis-directive.md) is one of the five hashed
      surfaces in the state snapshot.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

opportunity-analyst-jcode.sh runs the analyst via jcode with provider-specific credential and effort handling: Claude fails closed naming CLAUDE_CODE_OAUTH_TOKEN when no credential exists, OpenAI fails naming 'jcode login' without openai-auth.json, effort rides the provider-specific env var without leaking the other, and done.session_id lands exactly once in the sessions log (deduped). The report header names jcode/claude and the model claude-opus-5.

## Related

- produces [[state-snapshot-delta-probing]] — The analyst report (analysis-directive.md) is one of the five hashed surfaces in the state snapshot.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
