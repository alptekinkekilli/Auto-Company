---
name: KİK decision evidence pipeline
slug: ki-k-decision-evidence-pipeline
type: system
sources:
  - path: scripts/core/decision_text_hash.py
    hash: 790b22fa08940d8d4c5418ec441c98f9d119b33eb718b7cfde81c01c71d94922
  - path: scripts/ops/kik-decision-read.py
    hash: 4f2060cbaaa784433de9720f1e9a3bfb3ba6c06cab00fae0efa0a426e5c926de
sources_digest: 29bce193d5c60bd9e7bf52e9c353d21de59f11e0b8c1f585378295f1c8433681
links:
  - to: session-leak-scanning-evidence-integrity
    relation: implements
    description: >-
      The hash is the canonical evidence fingerprint; normalization order is
      load-bearing and must not be changed independently.
generator:
  version: 1
covers:
  - symbol: normalize
    kind: function
    at: 'scripts/core/decision_text_hash.py:L54-L60'
  - symbol: digest
    kind: function
    at: 'scripts/core/decision_text_hash.py:L63-L65'
  - symbol: fetch
    kind: function
    at: 'scripts/core/decision_text_hash.py:L68-L96'
  - symbol: main
    kind: function
    at: 'scripts/core/decision_text_hash.py:L99-L112'
  - symbol: _hasher
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L45-L51'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L54-L67'
  - symbol: text_of
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L70-L73'
  - symbol: first
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L76-L78'
  - symbol: field
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L81-L89'
  - symbol: read
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L92-L131'
  - symbol: main
    kind: function
    at: 'scripts/ops/kik-decision-read.py:L134-L159'
---
<!-- context:generated:start -->
## Summary

Fetches Turkish public procurement (KİK) decision pages and produces a compact, hash-verifiable digest. kik-decision-read uses curl with a browser UA (urllib fails TLS on macOS), retries short responses, and parses headers with exact regexes to avoid the intervening 'Mahkeme Kararları' block; the content hash is computed by dynamically importing decision_text_hash so it is guaranteed comparable to the bridge's recorded value. Exclusion sentences are extracted only after dropping quoted legislation so a quoted article is never mistaken for a real exclusion.

## Related

- implements [[session-leak-scanning-evidence-integrity]] — The hash is the canonical evidence fingerprint; normalization order is load-bearing and must not be changed independently.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
