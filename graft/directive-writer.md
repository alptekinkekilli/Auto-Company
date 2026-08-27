---
name: Directive Writer
slug: directive-writer
type: file
sources:
  - path: scripts/core/directive_writer.py
    hash: 447057795ab4776c589695bd00450009df0af8fff481fa7a68c89244ca93a9a3
sources_digest: f4f863d4df3fc313e0dd21bd4e126bc92b8f46cf056589dd04f736eba34c9ebd
links:
  - to: cockpit-dashboard
    relation: implements
    description: server.py routes directive writes through this writer.
  - to: opportunity-analyst
    relation: uses
    description: Used for safe restore of human-directive.md during analyst runs.
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
---
<!-- context:generated:start -->
## Summary

The single deterministic writer for memories/human-directive.md: locks, gates on in-flight PENDING directives, and refuses clobbering unless allow_pending is set. All dashboard and analyst writes route through it, and it is used for snapshot/restore guardrails.

## Related

- implements [[cockpit-dashboard]] — server.py routes directive writes through this writer.
- uses [[opportunity-analyst]] — Used for safe restore of human-directive.md during analyst runs.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
