---
name: jcode Pilot Smoke Test
slug: jcode-pilot-smoke-test
type: file
sources:
  - path: scripts/analyst/jcode-pilot-smoke.sh
    hash: 354473b12623cdd65b47b0245f7d2fe85e03182998cc3d114f5dd419ba944d99
sources_digest: 580997342635860ff744d27a36e889c902bd03a27837c94edb20c5bb745f01b5
links:
  - to: auto-loop-daemon
    relation: validates
    description: Verifies the jcode harness auto-loop.sh can drive.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Acceptance smoke test for the jcode pilot container verifying five checks while touching nothing persistent. Documents a key gotcha: as of jcode v0.64.2 the tool does NOT read the project's .mcp.json, so the script only verifies the file parses and registers servers — actual Airtable/Linear/BrowserOS connections are deferred to second-stage checks from the real host. Uses set -uo pipefail (deliberately omitting -e) and a 180-second timeout on the model call.

## Related

- validates [[auto-loop-daemon]] — Verifies the jcode harness auto-loop.sh can drive.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
