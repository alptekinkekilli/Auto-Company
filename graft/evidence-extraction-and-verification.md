---
name: Evidence extraction and verification
slug: evidence-extraction-and-verification
type: system
sources:
  - path: scripts/ops/extract-axis-evidence.py
    hash: 3f3d55a2a285cd52ab3b0d286b1f908b877283bfde69b03e442d10758080f567
  - path: scripts/ops/g4-check.py
    hash: 719fa86c0e307ef71bf0bce8f49e2baab2bb522aec732b784b39c8f2d788aba8
sources_digest: f67a2e23af4befe257a08e58bbc47e60c182803afdeadfe731c68b542417787a
links:
  - to: airtable-read-write-wrappers
    relation: uses
    description: g4-check.py pulls registry records via air_get/air_list.
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
---
<!-- context:generated:start -->
## Summary

Scripts that extract and verify evidence from discovery-scan markdown and Turkish firm sites. extract-axis-evidence.py extracts every screened axis heading and body, failing closed on any unreadable file/empty body/count mismatch (replacing a broken shell version that dropped kill reasons and missed 19 axes); g4-check.py automates G4 identity-attribution verdicts by testing a row's claim against live evidence (first-party contact plus address/registry-number/Profile-bridge anchor), reporting CLAIMED_PASS_UNVERIFIED rather than downgrading, with Turkish-aware normalization and authority-domain exclusion.

## Related

- uses [[airtable-read-write-wrappers]] — g4-check.py pulls registry records via air_get/air_list.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
