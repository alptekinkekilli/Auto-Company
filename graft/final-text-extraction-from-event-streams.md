---
name: Final-text extraction from event streams
slug: final-text-extraction-from-event-streams
type: concept
sources:
  - path: scripts/core/codex-final-text.py
    hash: 3bc904db8c553fb60846f122faadf8447d3fe045c99b4d47c906c67567c264e4
  - path: scripts/core/jcode-final-text.py
    hash: 8913ac57b8ca910581f28286fbdfb665674ee1a1273a477b39f39d1b02bf4215
sources_digest: 8c86c687652a082aa409b4a8ba8ffb34c64122612918dfab6b3f4384e3425870
links:
  - to: cost-budget-accounting
    relation: uses
    description: >-
      engine-usage-cost also parses the same jcode --ndjson stream, summing all
      tokens events.
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

Both codex and jcode emit NDJSON event streams where the 'final text' field is unreliable: done.text can silently truncate on tool-using runs (a measured 31-event text_delta sequence produced a full answer while done.text held only its last paragraph). jcode-final-text and codex-final-text concatenate all text deltas / agent_message events and prefer the longer reading, deliberately accepting pre-tool-call narration noise over content loss. Both are fail-soft (skip malformed lines, errors='replace') and exit 1 when no message is found so the caller falls back to raw content.

## Related

- uses [[cost-budget-accounting]] — engine-usage-cost also parses the same jcode --ndjson stream, summing all tokens events.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
