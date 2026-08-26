---
name: Compliance & Audit Watchers
slug: compliance-audit-watchers
type: system
sources:
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
  - path: scripts/ops/extract-axis-evidence.py
    hash: 3f3d55a2a285cd52ab3b0d286b1f908b877283bfde69b03e442d10758080f567
sources_digest: 6ad25135debc3010c3fb287b526134593c6ad7e08bfc4414954d327d335c821e
links:
  - to: cost-budget-ledger-adapters
    relation: uses
    description: >-
      cost-audit.py reads the same ndjson cycle logs and jcode logs these
      watchers parse.
generator:
  version: 1
covers:
  - symbol: externals
    kind: function
    at: 'scripts/ops/context7-check.py:L59-L75'
  - symbol: scan
    kind: function
    at: 'scripts/ops/context7-check.py:L78-L108'
  - symbol: walk_calls
    kind: function
    at: 'scripts/ops/context7-check.py:L111-L122'
  - symbol: verdict
    kind: function
    at: 'scripts/ops/context7-check.py:L125-L138'
  - symbol: main
    kind: function
    at: 'scripts/ops/context7-check.py:L141-L170'
  - symbol: key_phrases
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L49-L52'
  - symbol: covered
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L55-L68'
---
<!-- context:generated:start -->
## Summary

Deterministic compliance and audit watchers that parse on-disk logs and report, never judge or modify. context7-check.py detects code importing external libraries without first calling Context7 (avoiding prefiltering on exact JSON strings that caused false negatives). directive-rule-sweep.py audits rule-like statements not backed by standing docs, with a canary fixture to verify the heuristic. extract-axis-evidence.py fails closed on any unreadable file or count mismatch.

## Related

- uses [[cost-budget-ledger-adapters]] — cost-audit.py reads the same ndjson cycle logs and jcode logs these watchers parse.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
