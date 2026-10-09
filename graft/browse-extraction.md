---
name: Browse Extraction
slug: browse-extraction
type: file
sources:
  - path: tests/test_browse_extract.sh
    hash: 37b269657d3077acf85e81540cd0355f9e97b432f0e6e1d973c2dfc170a887a6
sources_digest: 079a0bb6c7007bc125906c31ea731cf2348652185ae27922be07b0c00c2cb0c9
links:
  - to: g4-attribution-evidence
    relation: uses
    description: >-
      Provides browser-based content extraction used in contact-evidence
      gathering
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

browse-extract.py drives a browser via MCP gateway to extract content, with the critical invariant that the browser tab is always closed even on error paths. Distinct exit codes for distinct failure modes (2 usage, 3 unreachable gateway, 4 tool error), truncation reports both capped and true content size, and multi-URL handling opens one tab then navigates for subsequent URLs.

## Related

- uses [[g4-attribution-evidence]] — Provides browser-based content extraction used in contact-evidence gathering
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
