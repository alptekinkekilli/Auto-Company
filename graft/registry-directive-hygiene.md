---
name: Registry & directive hygiene
slug: registry-directive-hygiene
type: system
sources:
  - path: scripts/ops/directive-rule-sweep.py
    hash: 7284bd834ff1cf86bcc5f6d104cf23388bf9258dcc827b681f578e6ce7172c57
  - path: scripts/ops/extract-axis-evidence.py
    hash: 3f3d55a2a285cd52ab3b0d286b1f908b877283bfde69b03e442d10758080f567
  - path: scripts/ops/registry-archive.py
    hash: 125be575d2da1c70effa433e2eabe55e5e7e7851fc89719651a1520bb76ee651
sources_digest: 52f5f2ef401cbc5fc72f21d9a1d1431f48a781ec656d8397b404908218423988
links:
  - to: operator-escalation-notification
    relation: uses
    description: >-
      Directive staleness and rule-sweep findings route to operator
      notifications.
generator:
  version: 1
covers:
  - symbol: key_phrases
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L49-L52'
  - symbol: covered
    kind: function
    at: 'scripts/ops/directive-rule-sweep.py:L55-L68'
  - symbol: die
    kind: function
    at: 'scripts/ops/registry-archive.py:L55-L57'
  - symbol: sha
    kind: function
    at: 'scripts/ops/registry-archive.py:L60-L61'
  - symbol: heading_line_starts
    kind: function
    at: 'scripts/ops/registry-archive.py:L64-L65'
  - symbol: protected_span
    kind: function
    at: 'scripts/ops/registry-archive.py:L68-L80'
  - symbol: plan_note_chunks
    kind: function
    at: 'scripts/ops/registry-archive.py:L83-L105'
  - symbol: plan_section_chunks
    kind: function
    at: 'scripts/ops/registry-archive.py:L108-L140'
  - symbol: interleave
    kind: function
    at: 'scripts/ops/registry-archive.py:L143-L149'
  - symbol: main
    kind: function
    at: 'scripts/ops/registry-archive.py:L152-L340'
  - symbol: month_of
    kind: function
    at: 'scripts/ops/registry-archive.py:L250-L251'
---
<!-- context:generated:start -->
## Summary

Maintenance and compliance tooling for the registry and directive files. registry-archive.py deterministically moves stale registry history into monthly archives, enforcing byte-identical protected regions and SHA-256 verification before any write. directive-rule-sweep.py audits which rule-like statements exist only in ephemeral directives and are not backed by standing docs, using a canary fixture to verify its heuristic. extract-axis-evidence.py rebuilds an evidence pack from discovery scans, failing closed on any heading/body mismatch.

## Related

- uses [[operator-escalation-notification]] — Directive staleness and rule-sweep findings route to operator notifications.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
