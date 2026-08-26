---
name: CLI Final-Text Extractors
slug: cli-final-text-extractors
type: concept
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
sources_digest: 50f7d26269f033eca96271260397036b6cb8e3cc93d3bb1d120e0c11189605b9
links:
  - to: autonomous-loop
    relation: uses
    description: >-
      auto-loop.sh uses these to extract final text from codex/jcode exec
      streams.
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

Two parallel extractors that pull the assistant's final text from CLI event streams that otherwise carry raw JSONL events: codex-final-text.py concatenates text fields of all item.completed agent_message events (ignoring reasoning/tool calls), and jcode-final-text.py mirrors it for the jcode path. Both fail-soft (skip malformed lines, tolerate schema changes) and concatenate all agent messages rather than picking just the last, following the principle that noise is never loss. Exit 1 if no agent message found so the caller falls back to raw file content.

## Related

- uses [[autonomous-loop]] — auto-loop.sh uses these to extract final text from codex/jcode exec streams.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
