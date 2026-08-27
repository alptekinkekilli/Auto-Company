---
name: Site contact evidence
slug: site-contact-evidence
type: system
sources:
  - path: scripts/ops/site-contact-evidence.py
    hash: 008b4735e6133445eff667f840f9c7faaeef8013b1363f6555b602a9d6fd048c
sources_digest: 5c3ab49bca83c326e54b9e154c81edea67c57863bcee0d19e964759966469ad2
links:
  - to: g4-identity-check
    relation: implements
    description: Provides the evidence-gathering step the G4 judge consumes.
generator:
  version: 1
covers:
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

Render-first examiner that fetches a firm's site and contact pages to extract first-party contact evidence, reused by g4-check.py.

## Related

- implements [[g4-identity-check]] — Provides the evidence-gathering step the G4 judge consumes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
