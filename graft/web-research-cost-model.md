---
name: Web research cost model
slug: web-research-cost-model
type: concept
sources:
  - path: scripts/ops/web-research-cost.py
    hash: 24d7735b6dc6defa0f80e75aeee37a13a40d4df43e9b38539be02df6fe23cbf2
sources_digest: 976169f8b29d99a352d9d4f4c66e56549da87c6f434116f4dfa18807078391d7
links:
  - to: budget-spend-accounting
    relation: uses
    description: feeds the same cost-per-token pricing assumptions
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

The true cost of a tool result scales with output size times remaining turns, because each result is re-read on every subsequent turn. web-research-cost.py scores all tools (not just web) since pre-filtering hid Airtable dumps as the largest context source.

## Related

- uses [[budget-spend-accounting]] — feeds the same cost-per-token pricing assumptions
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
