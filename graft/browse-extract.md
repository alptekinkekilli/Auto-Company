---
name: browse-extract
slug: browse-extract
type: system
sources:
  - path: scripts/ops/browse-extract.py
    hash: ec67b37ee0a24df3eb9d5b06f16e7172c456153e7c7b8bd61edc2b54f7543aa1
  - path: tests/test_browse_extract.sh
    hash: 37b269657d3077acf85e81540cd0355f9e97b432f0e6e1d973c2dfc170a887a6
sources_digest: c49e107369cdb204a557d35cefc2912be60f908dd3ecbd13bb775bee6cc668bc
links:
  - to: g4-attribution-contact-evidence
    relation: uses
    description: >-
      site-contact-evidence.py uses browser-rendered DOM via BrowserOS to find
      contact emails.
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

browse-extract.py drives a browser MCP gateway to extract page content, with the invariant that the browser tab is always closed even on error paths, distinct exit codes for distinct failure modes, and read truncation reporting both capped and true sizes.

## Related

- uses [[g4-attribution-contact-evidence]] — site-contact-evidence.py uses browser-rendered DOM via BrowserOS to find contact emails.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
