---
name: Graft auto-refresh hook
slug: graft-auto-refresh-hook
type: system
sources:
  - path: scripts/graft-auto-refresh.py
    hash: 678e4a269c718dc9043afa096157f5d835cb3099883d31954de70ff10a4bfe33
sources_digest: 349cf6c8fc1b8b2d774551e2842a1220b68910aa7da6e08ac140a57584d3d3b4
links: []
generator:
  version: 1
covers:
  - symbol: _repo_root
    kind: function
    at: 'scripts/graft-auto-refresh.py:L42-L54'
  - symbol: _git
    kind: function
    at: 'scripts/graft-auto-refresh.py:L57-L68'
  - symbol: _lock_alive
    kind: function
    at: 'scripts/graft-auto-refresh.py:L71-L81'
  - symbol: _emit
    kind: function
    at: 'scripts/graft-auto-refresh.py:L84-L94'
  - symbol: main
    kind: function
    at: 'scripts/graft-auto-refresh.py:L97-L187'
  - symbol: status
    kind: function
    at: 'scripts/graft-auto-refresh.py:L122-L132'
  - symbol: fmt
    kind: function
    at: 'scripts/graft-auto-refresh.py:L134-L137'
---
<!-- context:generated:start -->
## Summary

SessionStart hook that conditionally triggers a paid deep build of graft cards only when git history shows genuine staleness (commits-behind > 40 AND last graft commit age > 24h). Deliberately fail-open (always exits 0), non-blocking (launches detached), with lock and marker files preventing concurrent/rapid relaunches. The Together API key never touches this script (lives in graft-build.sh).
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
