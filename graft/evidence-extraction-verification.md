---
name: Evidence extraction & verification
slug: evidence-extraction-verification
type: system
sources:
  - path: scripts/ops/browse-extract.py
    hash: ec67b37ee0a24df3eb9d5b06f16e7172c456153e7c7b8bd61edc2b54f7543aa1
  - path: scripts/ops/extract-axis-evidence.py
    hash: 3f3d55a2a285cd52ab3b0d286b1f908b877283bfde69b03e442d10758080f567
sources_digest: fe32c044718f35762e1fb166e5fd82101189a8a900ccc665be4e0a5645260f88
links:
  - to: g4-identity-verification
    relation: uses
    description: >-
      g4-check reuses the render-first examiner site-contact-evidence.py to
      fetch firm site/contact pages.
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

Deterministic extraction of evidence from research and web sources. extract-axis-evidence.py pulls every screened axis heading and body from discovery-scan markdown with two regexes (AXIS_RE/STOP_RE), failing closed on any unreadable file, empty body, or count mismatch. browse-extract.py collapses the multi-turn MCP browse-and-extract workflow into one bash invocation via the BrowserOS MCP gateway, running server-side grep over rendered content (so SPAs are searched post-render) and reporting a timed-out wait as inconclusive rather than zero matches.

## Related

- uses [[g4-identity-verification]] — g4-check reuses the render-first examiner site-contact-evidence.py to fetch firm site/contact pages.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
