---
name: Compact Preflight
slug: compact-preflight
type: file
sources:
  - path: scripts/compact-preflight.py
    hash: e05718ceddc1954b8cefcea9ad00d143d0adb92d0d5547b55fe3916e5fbdb0b3
sources_digest: 8209b0e705f42296e979b77c5e321a326f8eb906c9d9dbc38000f6403c23136c
links:
  - to: context-watch
    relation: uses
    description: Consumed by the compact flow that context-watch.py triggers at 60%.
generator:
  version: 1
covers:
  - symbol: sh
    kind: function
    at: 'scripts/compact-preflight.py:L24-L28'
  - symbol: repo_report
    kind: function
    at: 'scripts/compact-preflight.py:L31-L48'
  - symbol: main
    kind: function
    at: 'scripts/compact-preflight.py:L51-L80'
---
<!-- context:generated:start -->
## Summary

Pre-flight check run from the PreCompact hook to make the compact ritual measurable: counts open items that would be lost if context is compacted without operator notification or agent recall. Builds a Markdown report per git root flagging unpushed commits, uncommitted tracked changes, and stash entries as risk items. Runs an optional .claude/preflight-extra.sh and counts its ⚠ occurrences. Report written to /tmp/compact-preflight.md for session-brief.py to read after compact; always exits 0 so it never blocks the compact itself.

## Related

- uses [[context-watch]] — Consumed by the compact flow that context-watch.py triggers at 60%.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
