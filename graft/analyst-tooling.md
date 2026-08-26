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
    description: >-
      context7_docs.sh provides library documentation context for the
      opportunity director skill.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Supporting scripts for the analyst and jcode pilot: context7_docs.sh wraps the Context7 API for library docs (key from env or macOS Keychain), and jcode-pilot-smoke.sh is the acceptance smoke test for the jcode pilot container verifying GLIBC sanity, binary runnability, Claude auth, a real model round-trip, and daemon-leak checks while touching nothing persistent. Documents the gotcha that jcode v0.64.2 does NOT read the project's .mcp.json.

## Related

- uses [[opportunity-analyst]] — context7_docs.sh provides library documentation context for the opportunity director skill.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
