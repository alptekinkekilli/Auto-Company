---
name: Codex/jcode Final-Text Extractors
slug: codex-jcode-final-text-extractors
type: system
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
sources_digest: 8c86c687652a082aa409b4a8ba8ffb34c64122612918dfab6b3f4384e3425870
links:
  - to: loop-driver
    relation: uses
    description: >-
      auto-loop.sh uses these to extract the final answer from engine event
      streams.
  - to: opportunity-analyst
    relation: uses
    description: The analyst runner uses jcode-final-text.py for the done event.
generator:
  version: 1
covers:
  - symbol: final_text
    kind: function
    at: 'scripts/core/codex-final-text.py:L30-L47'
  - symbol: main
    kind: function
    at: 'scripts/core/codex-final-text.py:L50-L60'
  - symbol: final_text
    kind: function
    at: 'scripts/core/jcode-final-text.py:L30-L48'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-final-text.py:L51-L61'
---
<!-- context:generated:start -->
## Summary

Small stdlib-only scripts that extract the assistant's final text from codex exec --json and jcode event streams, which otherwise carry raw JSONL events. Concatenate all agent_message text fields (noise is never loss) and fail soft on malformed lines; return exit 1 if no agent message is found so the caller can fall back to raw content.

## Related

- uses [[loop-driver]] — auto-loop.sh uses these to extract the final answer from engine event streams.
- uses [[opportunity-analyst]] — The analyst runner uses jcode-final-text.py for the done event.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
