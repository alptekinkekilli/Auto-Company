---
name: turn-audit regression suite
slug: turn-audit-regression-suite
type: system
sources:
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: 9e54d88a58a6833fd7953492436d5ad6088e09c805fe8290f0a77f63815c77ae
links:
  - to: turn-audit-policy-engine
    relation: validates
    description: Asserts verdict thresholds and boundary values against the audit script.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash regression tests for turn-audit.py. Generates synthetic daily-log lines via mkline/mk_session helpers, exercises session parsing, turn/message counting, cache accounting, and --summary-last, asserting verdict thresholds and that the newest session is selected. Includes a regression case where a previously mis-flagged healthy cycle must read 'ok'. Deliberately separates threshold-boundary tests from full-report tests.

## Related

- validates [[turn-audit-policy-engine]] — Asserts verdict thresholds and boundary values against the audit script.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
