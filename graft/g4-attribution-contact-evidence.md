---
name: G4 attribution & contact evidence
slug: g4-attribution-contact-evidence
type: system
sources:
  - path: scripts/ops/g4-check.py
    hash: 719fa86c0e307ef71bf0bce8f49e2baab2bb522aec732b784b39c8f2d788aba8
  - path: scripts/ops/site-contact-evidence.py
    hash: 008b4735e6133445eff667f840f9c7faaeef8013b1363f6555b602a9d6fd048c
sources_digest: 1627b649c4591fefbe53718943b83b073d34ecceb699cc194f34d1c884c4155e
links:
  - to: airtable-access-wrapper
    relation: uses
    description: Reads Outreach rows and Registry Bridge via Airtable.
  - to: outreach-eligibility-gate-send-gate-py
    relation: produces
    description: >-
      G4 verdict and contact evidence feed the eligibility decision and G4
      re-derivation.
generator:
  version: 1
covers:
  - symbol: load_key
    kind: function
    at: 'scripts/ops/g4-check.py:L71-L89'
  - symbol: norm
    kind: function
    at: 'scripts/ops/g4-check.py:L92-L100'
  - symbol: address_anchor
    kind: function
    at: 'scripts/ops/g4-check.py:L103-L132'
  - symbol: registry_id_anchor
    kind: function
    at: 'scripts/ops/g4-check.py:L135-L164'
  - symbol: field
    kind: function
    at: 'scripts/ops/g4-check.py:L167-L169'
  - symbol: domains_in
    kind: function
    at: 'scripts/ops/g4-check.py:L172-L180'
  - symbol: air_get
    kind: function
    at: 'scripts/ops/g4-check.py:L183-L187'
  - symbol: air_list
    kind: function
    at: 'scripts/ops/g4-check.py:L190-L195'
  - symbol: site_evidence
    kind: function
    at: 'scripts/ops/g4-check.py:L198-L217'
  - symbol: judge
    kind: function
    at: 'scripts/ops/g4-check.py:L220-L287'
  - symbol: main
    kind: function
    at: 'scripts/ops/g4-check.py:L290-L337'
  - symbol: fetch
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L56-L64'
  - symbol: emails
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L67-L68'
  - symbol: looks_unrendered
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L71-L81'
  - symbol: render_dom
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L84-L110'
  - symbol: examine
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L113-L172'
  - symbol: main
    kind: function
    at: 'scripts/ops/site-contact-evidence.py:L175-L196'
---
<!-- context:generated:start -->
## Summary

Determines whether a firm is G4 (government-affiliated) and finds published contact emails. site-contact-evidence.py escalates through browser-rendered DOM, raw HTML, and JS bundles, treating a fetch with no rendered content as inconclusive never negative. g4-check.py matches register address/registry IDs/domains with Turkish folding and coincidence guards.

## Related

- uses [[airtable-access-wrapper]] — Reads Outreach rows and Registry Bridge via Airtable.
- produces [[outreach-eligibility-gate-send-gate-py]] — G4 verdict and contact evidence feed the eligibility decision and G4 re-derivation.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
