---
name: jcode Pilot Smoke Test
slug: jcode-pilot-smoke-test
type: file
sources:
  - path: scripts/analyst/jcode-pilot-smoke.sh
    hash: 354473b12623cdd65b47b0245f7d2fe85e03182998cc3d114f5dd419ba944d99
sources_digest: 580997342635860ff744d27a36e889c902bd03a27837c94edb20c5bb745f01b5
links:
  - to: jcode-mcp-config
    relation: validates
    description: Verifies the generated MCP config parses and registers servers.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Acceptance smoke test for the jcode pilot container verifying five checks per RUNBOOK §0.4 while touching nothing persistent. Covers GLIBC sanity, jcode runnability, Claude auth (wrapping CLAUDE_CODE_OAUTH_TOKEN into a JSON blob with 300-day expiry), a real model round-trip, and a daemon-leak check. Uses set -uo pipefail (deliberately omitting -e) and a 180s timeout on the model call.

## Related

- validates [[jcode-mcp-config]] — Verifies the generated MCP config parses and registers servers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
