---
name: browse & extract harness
slug: browse-extract-harness
type: system
sources:
  - path: scripts/ops/browse-extract.py
    hash: ec67b37ee0a24df3eb9d5b06f16e7172c456153e7c7b8bd61edc2b54f7543aa1
  - path: scripts/ops/site-contact-evidence.py
    hash: 008b4735e6133445eff667f840f9c7faaeef8013b1363f6555b602a9d6fd048c
sources_digest: 9cfd9dd98ad1816eb5f8fc210cecd91d1be012c8cb7505985248885c06a68c8b
links:
  - to: outreach-eligibility-brake
    relation: uses
    description: >-
      site-contact-evidence.py's render-first examiner is reused by g4-check.py
      for contact evidence.
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
  - symbol: fetch
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L56-L64'
  - symbol: emails
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L67-L68'
  - symbol: looks_unrendered
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L71-L81'
  - symbol: render_dom
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L84-L110'
  - symbol: examine
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L113-L172'
  - symbol: main
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L175-L196'
---
<!-- context:generated:start -->
## Summary

CLI harnesses that collapse multi-step MCP workflows into single calls to cut context re-billing. browse-extract.py drives the BrowserOS MCP gateway (JSON-RPC over HTTP with session persistence) to open/navigate/wait/grep/read pages in one background tab, read-only by design, reporting a timed-out wait as inconclusive. site-contact-evidence.py escalates through rendered DOM, raw HTML, and JS bundles plus policy pages, treating rendering failure as non-fatal.

## Related

- uses [[outreach-eligibility-brake]] — site-contact-evidence.py's render-first examiner is reused by g4-check.py for contact evidence.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
