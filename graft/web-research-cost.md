---
name: Web research cost
slug: web-research-cost
type: file
sources:
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
sources_digest: 976169f8b29d99a352d9d4f4c66e56549da87c6f434116f4dfa18807078391d7
links:
  - to: airtable-access-wrappers
    relation: uses
    description: Scores Airtable read outputs as a context cost.
generator:
  version: 1
covers:
  - symbol: is_web
    kind: function
    at: 'scripts/ops/web-research-cost.py:L43-L44'
  - symbol: analyse
    kind: function
    at: 'scripts/ops/web-research-cost.py:L47-L76'
  - symbol: main
    kind: function
    at: 'scripts/ops/web-research-cost.py:L79-L161'
---
<!-- context:generated:start -->
## Summary

Measures the true cost of web research by scoring every tool call as output_tokens × turns_after_it × CACHE_READ_USD_PER_TOKEN, correcting the naive assumption that a fetch costs once. Deliberately scores all tools (not just web ones) because pre-filtering hid Airtable dumps as the largest context source.

## Related

- uses [[airtable-access-wrappers]] — Scores Airtable read outputs as a context cost.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
