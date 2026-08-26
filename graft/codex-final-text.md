---
name: Codex Final Text
slug: codex-final-text
type: file
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
sources_digest: 50f7d26269f033eca96271260397036b6cb8e3cc93d3bb1d120e0c11189605b9
links:
  - to: autonomous-loop
    relation: uses
    description: auto-loop.sh uses it to extract final text from codex exec --json.
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

Extracts assistant final text from codex exec --json event stream (raw JSONL events). Concatenates text fields of all item.completed agent_message events, ignoring reasoning/tool calls. Fail-soft on malformed lines; returns exit 1 if no agent message so caller falls back to raw file. Mirrors jcode-final-text.py for the older CLI path. Principle: noise is never loss.

## Related

- uses [[autonomous-loop]] — auto-loop.sh uses it to extract final text from codex exec --json.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
