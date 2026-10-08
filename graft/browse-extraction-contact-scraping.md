---
name: Browse Extraction & Contact Scraping
slug: browse-extraction-contact-scraping
type: system
sources:
  - path: scripts/ops/site-contact-evidence.py
    hash: 008b4735e6133445eff667f840f9c7faaeef8013b1363f6555b602a9d6fd048c
  - path: tests/test_browse_extract.sh
    hash: 37b269657d3077acf85e81540cd0355f9e97b432f0e6e1d973c2dfc170a887a6
sources_digest: 0f2989ca2baef2ca7956c3f882de6afb1178d77e20ec0f6320fb1ed1ba9bef27
links:
  - to: g4-attribution-contact-evidence
    relation: implements
    description: >-
      browse-extract and site-contact-evidence provide the browser-rendered
      contact evidence for G4 attribution.
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

browse-extract.py drives a browser MCP gateway to grep/read page content with a named byte cap, always closing the tab even on error paths (a critical invariant tested via a fake gateway), and site-contact-evidence.py escalates through rendered DOM, raw HTML, and JS bundles to find a firm's published contact email for G4 checks.

## Related

- implements [[g4-attribution-contact-evidence]] — browse-extract and site-contact-evidence provide the browser-rendered contact evidence for G4 attribution.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
