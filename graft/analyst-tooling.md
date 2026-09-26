---
name: Analyst Tooling
slug: analyst-tooling
type: system
sources:
  - path: >-
      scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
    hash: 79198378c25b2ff21cf5e4e2eda13f55c29ac806bd7f9d2bb0cba11a6268c447
  - path: scripts/analyst/jcode-pilot-smoke.sh
    hash: 354473b12623cdd65b47b0245f7d2fe85e03182998cc3d114f5dd419ba944d99
sources_digest: 86629429e8f655505e4d89df93ce8d4c5c5f8b8226a9c68464bda6fca19518fc
links:
  - to: opportunity-analyst
    relation: uses
    description: The skill directory synced for the analyst's codex/jcode runs.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Support scripts for the analyst and pilot: context7_docs.sh wraps the Context7 API (key from env or macOS Keychain) for library docs; jcode-pilot-smoke.sh is the acceptance smoke test for the jcode pilot container verifying GLIBC sanity, jcode runnability, Claude auth (wrapping CLAUDE_CODE_OAUTH_TOKEN into a JSON blob with 300-day expiry), a real model round-trip, and daemon-leak check — touching nothing persistent. Documents that jcode v0.64.2 does NOT read the project's .mcp.json, so only file-parse and server-registration are verified.

## Related

- uses [[opportunity-analyst]] — The skill directory synced for the analyst's codex/jcode runs.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
