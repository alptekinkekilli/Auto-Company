---
name: KİK Decision & Browser Extraction
slug: ki-k-decision-browser-extraction
type: system
sources:
  - path: scripts/ops/browse-extract.py
    hash: ec67b37ee0a24df3eb9d5b06f16e7172c456153e7c7b8bd61edc2b54f7543aa1
  - path: scripts/ops/kik-decision-read.py
    hash: 4f2060cbaaa784433de9720f1e9a3bfb3ba6c06cab00fae0efa0a426e5c926de
sources_digest: ea66efd50bd7f21ecdbf467423ca0449c09a7a2fafc96ab06ca47d55fb29e6bb
links:
  - to: outreach-eligibility-evidence
    relation: uses
    description: >-
      site-contact-evidence.py drives BrowserOS MCP via ekap-run.py, the same
      gateway browse-extract.py uses.
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
  - symbol: _hasher
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L45-L51'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L54-L67'
  - symbol: text_of
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L70-L73'
  - symbol: first
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L76-L78'
  - symbol: field
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L81-L89'
  - symbol: read
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L92-L131'
  - symbol: main
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L134-L159'
---
<!-- context:generated:start -->
## Summary

Single-call extraction utilities that avoid multi-turn browser round-trips that killed agent cycles. kik-decision-read.py fetches a Turkish procurement decision page with curl (urllib fails TLS on macOS), parsing header fields with exact regexes and dropping quoted legislation so a quoted article is never mistaken for a real exclusion. browse-extract.py collapses the browse-and-extract workflow into one bash invocation via the BrowserOS MCP gateway, read-only by design, reporting timed-out waits as inconclusive.

## Related

- uses [[outreach-eligibility-evidence]] — site-contact-evidence.py drives BrowserOS MCP via ekap-run.py, the same gateway browse-extract.py uses.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
