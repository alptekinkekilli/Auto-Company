---
name: browse-extract harness
slug: browse-extract-harness
type: file
sources:
  - path: scripts/ops/browse-extract.py
    hash: ec67b37ee0a24df3eb9d5b06f16e7172c456153e7c7b8bd61edc2b54f7543aa1
sources_digest: 7514f4be06d24fc6714b50b6a7ae6ea56f424c1b9ce6bc87210364785a9290f3
links:
  - to: outreach-eligibility-g4-verification
    relation: uses
    description: >-
      site-contact-evidence.py drives BrowserOS MCP through the same gateway for
      rendered-DOM contact extraction.
generator:
  version: 1
covers:
  - symbol: Gateway
    kind: class
    at: 'scripts/ops/browse-extract.py:L45-L83'
  - symbol: __init__
    kind: method
    at: 'scripts/ops/browse-extract.py:L46-L49'
  - symbol: post
    kind: method
    at: 'scripts/ops/browse-extract.py:L51-L67'
  - symbol: call
    kind: method
    at: 'scripts/ops/browse-extract.py:L69-L77'
  - symbol: handshake
    kind: method
    at: 'scripts/ops/browse-extract.py:L79-L83'
  - symbol: clip
    kind: function
    at: 'scripts/ops/browse-extract.py:L86-L91'
  - symbol: extract
    kind: function
    at: 'scripts/ops/browse-extract.py:L94-L119'
  - symbol: ToolError
    kind: class
    at: 'scripts/ops/browse-extract.py:L122-L123'
  - symbol: main
    kind: function
    at: 'scripts/ops/browse-extract.py:L126-L201'
---
<!-- context:generated:start -->
## Summary

Collapses the multi-step MCP browse-and-extract workflow into one bash invocation, cutting context re-billing from ~5-9 turns per page to one. Read-only by design, runs server-side grep over rendered content so SPAs are searched post-render, and reports a timed-out wait as inconclusive rather than zero matches.

## Related

- uses [[outreach-eligibility-g4-verification]] — site-contact-evidence.py drives BrowserOS MCP through the same gateway for rendered-DOM contact extraction.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
