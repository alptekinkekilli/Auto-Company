---
name: Evidence extraction & axis screening
slug: evidence-extraction-axis-screening
type: system
sources:
  - path: scripts/ops/extract-axis-evidence.py
    hash: 3f3d55a2a285cd52ab3b0d286b1f908b877283bfde69b03e442d10758080f567
sources_digest: 4bf6158710472fff59770fd8e5c297877f60bc810d6cb8cf5efc464a05a6a1b0
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Two scripts supporting research evidence handling: extract-axis-evidence.py extracts every screened axis heading and body from discovery-scan markdown files, failing closed on any unreadable file, empty body, or heading/body count mismatch so output never silently omits evidence (replacing a broken shell version that dropped kill reasons and missed 19 axes); kik-decision-read.py (covered separately) fetches procurement decisions. Both are stdlib-only and strict-validation-over-silent-success.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
