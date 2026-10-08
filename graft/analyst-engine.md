---
name: Analyst Engine
slug: analyst-engine
type: system
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 8250db61c0a1031c088076e240616d2771868957339ff80f5e730388b06e5395
  - path: tests/test_analyst_engine.sh
    hash: 3f6fbcc1efd4568252ac5d138931953946575646f3cdd0edd9f2a3bbe325cf63
sources_digest: 24e5cf415f1f3114f9283e91276213f80f34d7f0fcc25c5d4753b7b247f1c154
links:
  - to: state-snapshot-consensus
    relation: produces
    description: >-
      The analyst report is written to memories/analysis-directive.md, whose
      hash is one of the five watched surfaces in state-snapshot.py.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The analyst opportunity engine (scripts/analyst/opportunity-analyst-jcode.sh) that runs jcode with provider-specific credential handling: the Claude default provider fails closed naming CLAUDE_CODE_OAUTH_TOKEN when no credential exists, the OpenAI provider without openai-auth.json fails naming 'jcode login', and effort rides the provider-specific env var without leaking the other. The done.session_id from the stub's ndjson stream lands exactly once in the sessions log (deduped), and the report header names jcode/claude and the model claude-opus-5.

## Related

- produces [[state-snapshot-consensus]] — The analyst report is written to memories/analysis-directive.md, whose hash is one of the five watched surfaces in state-snapshot.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
