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
  - path: scripts/core/bridge_leak_scan.py
    hash: e5b7b7ecf614217b79e93037d780bdd0314f4953d8e6308939a49fe5b5b92bcf
sources_digest: cc88ad9de752b39fbcb7c2a2949f7a9bdd27b9c1d03b9f793319c8b9a4d58d04
links:
  - to: autonomous-loop
    relation: uses
    description: bridge_leak_scan.py scans session output for credential leaks.
  - to: opportunity-analyst
    relation: uses
    description: >-
      context7_docs.sh provides library-doc context for the opportunity director
      skill.
generator:
  version: 1
covers:
  - symbol: scan
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L63-L69'
  - symbol: selftest
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L98-L111'
  - symbol: main
    kind: function
    at: 'scripts/core/bridge_leak_scan.py:L114-L127'
---
<!-- context:generated:start -->
## Summary

Supporting scripts for the analyst and loop: context7_docs.sh (CLI wrapping the Context7 API for library docs, key from env or macOS Keychain), jcode-pilot-smoke.sh (acceptance smoke test for the jcode pilot container verifying GLIBC sanity, binary runnability, Claude auth via wrapped OAuth token, a real model round-trip, and daemon-leak check — touches nothing persistent), and bridge_leak_scan.py (value-sensitive session-leak scanner for EKAP Bridge records flagging only key-plus-value adjacencies, with embedded selftest fixtures that gate trust).

## Related

- uses [[autonomous-loop]] — bridge_leak_scan.py scans session output for credential leaks.
- uses [[opportunity-analyst]] — context7_docs.sh provides library-doc context for the opportunity director skill.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
