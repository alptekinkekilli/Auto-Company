---
name: Engine Final-Text Extractors
slug: engine-final-text-extractors
type: concept
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
sources_digest: 50f7d26269f033eca96271260397036b6cb8e3cc93d3bb1d120e0c11189605b9
links: []
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

Pair of scripts (codex-final-text.py and jcode-final-text.py) that extract the assistant's final text from raw JSONL event streams, which otherwise carry events instead of a plain answer. Both concatenate all agent_message text fields (noise is never loss), fail soft on malformed lines, and return exit 1 if no agent message is found so the caller falls back to raw file content.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
