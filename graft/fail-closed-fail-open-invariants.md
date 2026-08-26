---
name: fail-closed & fail-open invariants
slug: fail-closed-fail-open-invariants
type: concept
sources:
  - path: scripts/core/auto-loop.sh
    hash: 19f2148376589dba4de398b1ec4040b9419c62ea0a03089842cc8978b006f8b0
  - path: scripts/core/jcode-mcp-config.py
    hash: 69e213cd234def194fee047d846a0c29f3c11edb07d7c7421fde188d1f75121c
  - path: scripts/ops/send-gate.py
    hash: 6acd746a20aff7267d711d61350ac14d8fa0c17a1af95341625aa2bfd9a63f92
  - path: scripts/prod-mechanism-guard.py
    hash: df90f44c6e799ee5505f180b9c47889d0ebfe295a0fd99b661438f51a8dd6bf2
  - path: tests/test_active_window.sh
    hash: fcd17dad9794b155cb623d85a88dd74bf10c12961df71a37f446f030958135fd
  - path: tests/test_ccusage_failclosed.sh
    hash: 366b96bee74416db05cc9752919b04304a49f5121d5802920a26641b196ef706
  - path: tests/test_idle_skip.sh
    hash: 13ce9f0b8801b94a1bc896bd2db53f2fc68c2984b45db8372050ca760e1edb53
  - path: tests/test_send_gate.sh
    hash: 4d0f03bd1b3e73a289e87cf0a56b25499b131e48fac01098b3f1d81755cb190d
sources_digest: de47ea6310218f96572596b3d1ddbadaa0a5333df293fad232a816aa07a11225
links:
  - to: budget-spend-accounting
    relation: implements
    description: >-
      ccusage fail-closed behavior and never-lower-prior are the canonical
      instance.
  - to: outreach-send-gate
    relation: implements
    description: send-gate refuses on any unknown or error.
generator:
  version: 1
covers:
  - symbol: expand
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L82-L94'
  - symbol: sub
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L86-L91'
  - symbol: convert
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L97-L148'
  - symbol: main
    kind: function
    at: 'scripts/core/jcode-mcp-config.py:L151-L258'
  - symbol: phase_of
    kind: function
    at: 'scripts/ops/send-gate.py:L66-L91'
  - symbol: body_claims
    kind: function
    at: 'scripts/ops/send-gate.py:L94-L101'
  - symbol: load_key
    kind: function
    at: 'scripts/ops/send-gate.py:L104-L122'
  - symbol: air
    kind: function
    at: 'scripts/ops/send-gate.py:L125-L135'
  - symbol: sent_rows
    kind: function
    at: 'scripts/ops/send-gate.py:L138-L148'
  - symbol: logged_sends
    kind: function
    at: 'scripts/ops/send-gate.py:L154-L177'
  - symbol: counts
    kind: function
    at: 'scripts/ops/send-gate.py:L180-L198'
  - symbol: opted_out
    kind: function
    at: 'scripts/ops/send-gate.py:L201-L215'
  - symbol: body_leak_scan
    kind: function
    at: 'scripts/ops/send-gate.py:L236-L244'
  - symbol: g4_live
    kind: function
    at: 'scripts/ops/send-gate.py:L247-L309'
  - symbol: decide
    kind: function
    at: 'scripts/ops/send-gate.py:L312-L544'
  - symbol: main
    kind: function
    at: 'scripts/ops/send-gate.py:L547-L583'
  - symbol: is_protected
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L48-L51'
  - symbol: check_sync
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L54-L80'
  - symbol: main
    kind: function
    at: 'scripts/prod-mechanism-guard.py:L83-L125'
---
<!-- context:generated:start -->
## Summary

A cross-cutting design principle: measurement and gating paths fail closed (ccusage failure latches a hold and returns NA not 0; degraded reads never lower a same-period prior; send-gate refuses on any unknown/error; MCP config refuses to write partial output), while availability paths fail open (malformed window config keeps the gate active; prod-mechanism guard fails open in-container; idle check treats unavailable snapshot as not idle). The distinction is deliberate and tested per surface.

## Related

- implements [[budget-spend-accounting]] — ccusage fail-closed behavior and never-lower-prior are the canonical instance.
- implements [[outreach-send-gate]] — send-gate refuses on any unknown or error.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
