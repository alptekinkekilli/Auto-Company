---
name: Context7 Import Audit
slug: context7-import-audit
type: file
sources:
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
sources_digest: 0491c4407e0fe69bcc8291502ec69f7a3a70a54cb2d14a35aae791d02d5557e2
links:
  - to: auto-company-ops-scripts
    relation: validates
    description: Audits cycles for Context7 documentation lookups on external imports.
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

context7-check.py audits assistant cycles to ensure external library imports are accompanied by a Context7 documentation lookup, flagging external imports without a check as CONTEXT7 NO-CHECK. It deliberately must not fire on the project's own stdlib-only ops scripts to avoid false alarms that erode trust, and parses payloads via JSON not regex.

## Related

- validates [[auto-company-ops-scripts]] — Audits cycles for Context7 documentation lookups on external imports.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
