---
name: auto_loop
slug: auto-loop
type: system
sources:
  - path: docker-entrypoint.sh
    hash: fbc2010d8d1d9dda2bc7ebd72fba1d674136624f968ff2f453bf7bbb894de017
  - path: scripts/core/auto-loop.sh
    hash: b8f8a3989fee29f5a561d7f4d4eb8f558086586d603c5217caf20288b84d27ec
  - path: tests/test_prompt_assembly.sh
    hash: 0cd8e397ee0db20d70eac066f7542b6dbabfec6bdd6d031cdc0e378da04876d6
  - path: tests/test_prompt_transport.sh
    hash: c5df34a0acc0d09b63a231df392960370ab146ceea135b5bcace427223300501
  - path: tests/test_seteshape_lint.py
    hash: c75dd121edbe7aed5432f718bdfff952149464b77f9ab22baced3682261ebc98
  - path: tests/test_tier_ladder_daily.sh
    hash: d0bfb4ace48e1fa9665e17059be3f618b46fda0dcf432544a6bb16c07a3ed8db
sources_digest: 76d3169bfa9656c0be9ccb1c7023bf40329bf6aba1d796995e4fba677806dcef
links:
  - to: operator-request-notify
    relation: uses
    description: >-
      The loop's consensus projection is produced from operator_request_notify's
      resolution state.
  - to: set-e-shape-lint
    relation: validates
    description: >-
      The set-e-shape lint scans auto-loop.sh and docker-entrypoint.sh for the
      fatal '[ test ] && action' pattern that killed an unguarded caller in
      APP-240.
generator:
  version: 1
covers:
  - symbol: _is_fatal_shape
    kind: function
    at: 'tests/test_seteshape_lint.py:L42-L43'
  - symbol: _executable_lines
    kind: function
    at: 'tests/test_seteshape_lint.py:L46-L52'
  - symbol: find_violations
    kind: function
    at: 'tests/test_seteshape_lint.py:L55-L84'
  - symbol: SetEShapeLint
    kind: class
    at: 'tests/test_seteshape_lint.py:L87-L99'
  - symbol: test_no_fatal_test_and_shapes
    kind: method
    at: 'tests/test_seteshape_lint.py:L88-L99'
---
<!-- context:generated:start -->
## Summary

The core orchestration loop (scripts/core/auto-loop.sh) that assembles FULL_PROMPT from guardrails, consensus, snapshot, and cycle_orders; transports prompts to engine CLIs (claude/codex via STDIN to avoid E2BIG, jcode via run subcommand argv with a 126000-byte guard); and applies the daily-budget tier ladder (APP-263). It is the subject of several regression tests because a stray double quote in a guardrail once closed an assignment early and caused a production outage that bash -n could not detect.

## Related

- uses [[operator-request-notify]] — The loop's consensus projection is produced from operator_request_notify's resolution state.
- validates [[set-e-shape-lint]] — The set-e-shape lint scans auto-loop.sh and docker-entrypoint.sh for the fatal '[ test ] && action' pattern that killed an unguarded caller in APP-240.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
