---
name: CLI Final-Text Extractors
slug: cli-final-text-extractors
type: system
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
sources_digest: 50f7d26269f033eca96271260397036b6cb8e3cc93d3bb1d120e0c11189605b9
links:
  - to: auto-loop
    relation: uses
    description: auto-loop.sh uses these to get plain answers from JSONL streams.
  - to: opportunity-analyst
    relation: uses
    description: extract_final_text delegates to jcode-final-text.py.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
---
<!-- context:generated:start -->
## Summary

Extract the assistant's final text from raw JSONL event streams (codex exec --json and jcode), concatenating all agent_message events rather than picking the last — 'noise is never loss'. Fail-soft on malformed lines and return exit 1 when no agent message is found so callers fall back to raw content.

## Related

- uses [[auto-loop]] — auto-loop.sh uses these to get plain answers from JSONL streams.
- uses [[opportunity-analyst]] — extract_final_text delegates to jcode-final-text.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
