---
name: session & context tooling
slug: session-context-tooling
type: system
sources:
  - path: scripts/core/directive_writer.py
    hash: 447057795ab4776c589695bd00450009df0af8fff481fa7a68c89244ca93a9a3
  - path: scripts/ops/context7-check.py
    hash: 4687b776e558caf660fad0d984e405c6a9498525648273569ac9a5feb544797e
  - path: scripts/session-brief.py
    hash: a6cd13941a50d768403e080d89e484683b33ec725c6ce151e4447074b784cea4
  - path: tests/test_context7_check.sh
    hash: d4fc93cf6b456038f23e1e756019a7fa1b47a344b0385bc5cd3d3a5536834733
  - path: tests/test_directive_section_refs.sh
    hash: 413742241d956ae77feb01e20780757ee86fa63f3699e3926a2ddeea81a53a71
sources_digest: d4d4875667554bc2d859fb7fe7dde61b1e9059ae6dd4b9c75118a4217ca292d8
links:
  - to: auto-loop-core-loop
    relation: uses
    description: >-
      directive_writer maintains the directive that auto-loop reads;
      context7-check audits cycle NDJSON.
  - to: prod-mechanism-guard
    relation: part_of
    description: All are Claude Code hooks/context tooling in scripts/.
generator:
  version: 1
covers:
  - symbol: undefined_section_refs
    kind: function
    at: 'scripts/core/directive_writer.py:L74-L83'
  - symbol: now
    kind: function
    at: 'scripts/core/directive_writer.py:L86-L87'
  - symbol: sha
    kind: function
    at: 'scripts/core/directive_writer.py:L90-L91'
  - symbol: read_live
    kind: function
    at: 'scripts/core/directive_writer.py:L94-L100'
  - symbol: body_of
    kind: function
    at: 'scripts/core/directive_writer.py:L103-L110'
  - symbol: audit
    kind: function
    at: 'scripts/core/directive_writer.py:L113-L119'
  - symbol: _telegram_env
    kind: function
    at: 'scripts/core/directive_writer.py:L122-L145'
  - symbol: notify
    kind: function
    at: 'scripts/core/directive_writer.py:L148-L158'
  - symbol: _why_pending
    kind: function
    at: 'scripts/core/directive_writer.py:L161-L189'
  - symbol: backup
    kind: function
    at: 'scripts/core/directive_writer.py:L192-L206'
  - symbol: normalize_ownership
    kind: function
    at: 'scripts/core/directive_writer.py:L209-L255'
  - symbol: atomic_write
    kind: function
    at: 'scripts/core/directive_writer.py:L258-L270'
  - symbol: verify_written
    kind: function
    at: 'scripts/core/directive_writer.py:L273-L277'
  - symbol: Refused
    kind: class
    at: 'scripts/core/directive_writer.py:L280-L281'
  - symbol: with_lock
    kind: function
    at: 'scripts/core/directive_writer.py:L284-L293'
  - symbol: wrapper
    kind: function
    at: 'scripts/core/directive_writer.py:L285-L292'
  - symbol: cmd_write
    kind: function
    at: 'scripts/core/directive_writer.py:L306-L359'
  - symbol: cmd_status
    kind: function
    at: 'scripts/core/directive_writer.py:L363-L397'
  - symbol: cmd_restore
    kind: function
    at: 'scripts/core/directive_writer.py:L401-L437'
  - symbol: cmd_show
    kind: function
    at: 'scripts/core/directive_writer.py:L440-L445'
  - symbol: main
    kind: function
    at: 'scripts/core/directive_writer.py:L448-L495'
  - symbol: _refuse_forbidden
    kind: function
    at: 'scripts/core/directive_writer.py:L476-L482'
  - symbol: fn
    kind: function
    at: 'scripts/core/directive_writer.py:L477-L481'
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
  - symbol: sh
    kind: function
    at: 'scripts/session-brief.py:L19-L23'
  - symbol: main
    kind: function
    at: 'scripts/session-brief.py:L26-L63'
---
<!-- context:generated:start -->
## Summary

session-brief.py (SessionStart hook) injects a measured real-time git-state brief, never blocks, never writes secrets, and states that measurements override summary text; directive_writer.py maintains the directive with undefined_section_refs() guarding against the revision-11 freeze bug; context7-check.py audits cycles to ensure external imports are accompanied by a Context7 lookup, staying silent on the project's own stdlib-only ops scripts to avoid false alarms.

## Related

- uses [[auto-loop-core-loop]] — directive_writer maintains the directive that auto-loop reads; context7-check audits cycle NDJSON.
- part of [[prod-mechanism-guard]] — All are Claude Code hooks/context tooling in scripts/.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
