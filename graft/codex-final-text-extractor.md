---
name: Codex Final Text Extractor
slug: codex-final-text-extractor
type: file
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
sources_digest: 50f7d26269f033eca96271260397036b6cb8e3cc93d3bb1d120e0c11189605b9
links:
  - to: auto-loop
    relation: implements
    description: Used by auto-loop.sh to extract the CLI path's final answer.
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

Extracts the assistant's final text from a codex exec --json event stream by concatenating text fields of item.completed agent_message events, ignoring reasoning/tool calls. Returns exit 1 if no agent message found so the caller falls back to raw content. Fail-soft (skips malformed lines); concatenates all agent messages rather than just the last — noise is never loss. Mirrors jcode-final-text.py.

## Related

- implements [[auto-loop]] — Used by auto-loop.sh to extract the CLI path's final answer.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
