---
name: Context7 Docs CLI
slug: context7-docs-cli
type: file
sources:
  - path: >-
      scripts/analyst/codex-skill/autocompany-opportunity-director/scripts/context7_docs.sh
    hash: 79198378c25b2ff21cf5e4e2eda13f55c29ac806bd7f9d2bb0cba11a6268c447
sources_digest: d015b3a02ab7360603b113092f672eafcdd3a21270b3ab056880f098f44b12c1
links:
  - to: opportunity-analyst
    relation: uses
    description: >-
      The opportunity-director skill uses this CLI to fetch library docs
      context.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

A Bash wrapper around the Context7 API for fetching library documentation context, with check/search/docs subcommands. Resolves the API key via env var or the macOS Keychain, uses strict argument validation and set -euo pipefail, and falls back to plain text when jq is absent.

## Related

- uses [[opportunity-analyst]] — The opportunity-director skill uses this CLI to fetch library docs context.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
