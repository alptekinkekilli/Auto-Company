---
name: jcode Pilot Smoke Test
slug: jcode-pilot-smoke-test
type: file
sources:
  - path: scripts/analyst/jcode-pilot-smoke.sh
    hash: 354473b12623cdd65b47b0245f7d2fe85e03182998cc3d114f5dd419ba944d99
sources_digest: 580997342635860ff744d27a36e889c902bd03a27837c94edb20c5bb745f01b5
links:
  - to: autonomous-loop
    relation: validates
    description: Validates the jcode harness used by the loop.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Acceptance smoke test for the jcode pilot container (autocompany-jcode:pilot), verifying five checks per RUNBOOK §0.4 while touching nothing persistent. Covers GLIBC sanity, jcode binary runnability, Claude auth (wrapping CLAUDE_CODE_OAUTH_TOKEN in JSON blob with 300-day expiry), real model round-trip against claude-haiku-4-5-20251001, daemon-leak check. Documents gotcha: as of jcode v0.64.2 the tool does NOT read project .mcp.json, so only verifies file parses and registers servers — actual Airtable/Linear/BrowserOS connections deferred to host-side second-stage checks.

## Related

- validates [[autonomous-loop]] — Validates the jcode harness used by the loop.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
