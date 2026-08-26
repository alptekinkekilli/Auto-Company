---
name: Analyst Final-Text Extraction
slug: analyst-final-text-extraction
type: concept
sources:
  - path: scripts/analyst/opportunity-analyst-jcode.sh
    hash: 69985d473943f6d5adc94f51728ad97490391d0f517750ce54c9b785931bf5d6
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
sources_digest: 6b5c23a493de6d1a5aa2058a2aabd5bd7c9b1f9ecde03598b04d56c561605327
links:
  - to: auto-loop
    relation: uses
    description: >-
      auto-loop.sh falls back to raw file content when no agent message is
      found.
  - to: opportunity-analyst
    relation: uses
    description: >-
      opportunity-analyst-jcode.sh delegates to jcode-final-text.py to extract
      the final answer.
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

Cross-cutting pattern of extracting the assistant's final answer from raw JSONL event streams (codex exec --json and jcode ndjson), since these CLIs emit events rather than a plain answer. Both codex-final-text.py and jcode-final-text.py concatenate all agent_message text fields (noise is never loss), ignore reasoning/tool events, and fail soft on malformed lines. The jcode variant is invoked by the analyst runner to pull the final answer from the done event.

## Related

- uses [[auto-loop]] — auto-loop.sh falls back to raw file content when no agent message is found.
- uses [[opportunity-analyst]] — opportunity-analyst-jcode.sh delegates to jcode-final-text.py to extract the final answer.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
