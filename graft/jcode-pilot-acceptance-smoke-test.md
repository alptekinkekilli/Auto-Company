---
name: jcode pilot acceptance smoke test
slug: jcode-pilot-acceptance-smoke-test
type: system
sources:
  - path: scripts/analyst/jcode-pilot-smoke.sh
    hash: 354473b12623cdd65b47b0245f7d2fe85e03182998cc3d114f5dd419ba944d99
sources_digest: 580997342635860ff744d27a36e889c902bd03a27837c94edb20c5bb745f01b5
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The acceptance smoke test for the jcode pilot container, verifying five checks per RUNBOOK §0.4 while touching nothing persistent: GLIBC sanity, jcode runnability, Claude auth via wrapped OAuth token, a real model round-trip, and a daemon-leak check. Documents the gotcha that jcode v0.64.2 does NOT read the project's .mcp.json, so only file parsing/registration is verified here.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
