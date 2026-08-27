---
name: SnapOG Landing
slug: snapog-landing
type: system
sources:
  - path: projects/_archive/snapog/sample/alerts-dry-run.sh
    hash: fabd322c673a2e7f93273116221eac10392cdbf3d6cd8eb5457e6c960b67797c
  - path: projects/_archive/snapog/sample/cache-cap-test.sh
    hash: c11830b054136c0d367415ca1a62bc16312be6ec69c45fc217b2fda9bf8a67bc
  - path: projects/_archive/snapog/sample/smoke-test.sh
    hash: 0a140d23218574add9c22c524d6ff03aea85a205f4806261fc0791a4b73c144f
  - path: projects/_archive/snapog/src/dashboard/pages.ts
    hash: 6a33d1b6152ee8ea3ee6f5617105ce757c915627156072dd9cb1f3b78e32b4af
sources_digest: 549070e3b2562d329888a889272968ce40f9a958654aa3bb1b592200e5288d75
links:
  - to: snapog-service
    relation: uses
    description: >-
      Landing page hits the /og endpoint for live preview; waitlist stores to
      KV.
generator:
  version: 1
covers:
  - symbol: layout
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L340-L355'
  - symbol: nav
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L357-L367'
  - symbol: footer
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L369-L376'
  - symbol: landingPage
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L378-L588'
  - symbol: registerPage
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L590-L628'
  - symbol: keyCreatedPage
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L630-L700'
  - symbol: dashboardPage
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L702-L789'
  - symbol: errorPage
    kind: function
    at: 'projects/_archive/snapog/src/dashboard/pages.ts:L791-L805'
---
<!-- context:generated:start -->
## Summary

Server-side HTML template module rendering the public landing page and dashboard with a Carbon Terminal aesthetic, plus the waitlist capture function and smoke-test scripts. No client-side framework; host threaded into code examples for absolute URLs.

## Related

- uses [[snapog-service]] — Landing page hits the /og endpoint for live preview; waitlist stores to KV.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
