---
name: turn-audit regression suite
slug: turn-audit-regression-suite
type: file
sources:
  - path: tests/test_turn_audit.sh
    hash: ce3eb2af3fea266a763a0ca266f3c658f8498b604570c229141654d685f6c9e8
sources_digest: 9e54d88a58a6833fd7953492436d5ad6088e09c805fe8290f0a77f63815c77ae
links:
  - to: turn-audit-policy-script
    relation: validates
    description: >-
      Depends on python3 and the audit script; fails loudly via a contains
      helper if any assertion fails, and separates threshold-boundary tests from
      full-report tests.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Bash regression test for turn-audit.py. Generates synthetic daily-log lines via mkline/mk_session to exercise session parsing, turn/message counting, cache accounting, and --summary-last, asserting the newest session is selected and verdict thresholds apply. Pins specific boundary values and includes a regression case where a previously mis-flagged healthy cycle must read ok.

## Related

- validates [[turn-audit-policy-script]] — Depends on python3 and the audit script; fails loudly via a contains helper if any assertion fails, and separates threshold-boundary tests from full-report tests.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
