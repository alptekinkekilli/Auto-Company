---
name: Airtable Ops
slug: airtable-ops
type: system
sources:
  - path: tests/test_airtable_read.sh
    hash: f1c8fbb1b495e922c52d041bac7edbae8f100ab57606ebd987179783265325df
  - path: tests/test_airtable_write.sh
    hash: a51c25001935da566cca4a450cfc0906827eb332779f2b454b12d547b7a0e6e0
sources_digest: f36a07c38e3cd5b13c9c5c2ebd4240613fd28de5db52e96debd23170ea040e77
links:
  - to: mcp-configuration
    relation: uses
    description: >-
      Airtable is one of the four required MCP servers in .mcp.json, with
      Keychain fallback on macOS.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

The Airtable read/write wrappers that gate context costs and validate writes. airtable-read.py scopes reads (200-record cap, 100 pageSize, --all-fields capped unless --force); airtable-write.py's guard validates single-record writes offline (unknown fields, --allow-clear, --replace).

## Related

- uses [[mcp-configuration]] — Airtable is one of the four required MCP servers in .mcp.json, with Keychain fallback on macOS.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
