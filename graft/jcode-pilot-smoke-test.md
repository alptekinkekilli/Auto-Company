---
name: jcode Pilot Smoke Test
slug: jcode-pilot-smoke-test
type: file
sources:
  - path: scripts/analyst/jcode-pilot-smoke.sh
    hash: 354473b12623cdd65b47b0245f7d2fe85e03182998cc3d114f5dd419ba944d99
sources_digest: 580997342635860ff744d27a36e889c902bd03a27837c94edb20c5bb745f01b5
links:
  - to: loop-driver
    relation: validates
    description: Validates the jcode harness used by auto-loop.sh and the analyst runner.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Acceptance smoke test for the jcode pilot container verifying five checks (GLIBC sanity, binary runnability, Claude auth via OAuth token envelope, a real model round-trip, daemon-leak check) while touching nothing persistent. Documents a gotcha: as of jcode v0.64.2 the tool does NOT read the project's .mcp.json, so it only verifies the file parses — actual MCP connections are deferred to host-side checks.

## Related

- validates [[loop-driver]] — Validates the jcode harness used by auto-loop.sh and the analyst runner.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
