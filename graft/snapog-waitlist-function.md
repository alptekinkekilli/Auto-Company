---
name: SnapOG Waitlist Function
slug: snapog-waitlist-function
type: file
sources:
  - path: projects/_archive/snapog/src/dashboard/pages.ts
    hash: 6a33d1b6152ee8ea3ee6f5617105ce757c915627156072dd9cb1f3b78e32b4af
sources_digest: aa49b78a6522f0383edeedf2bbb936457599ccfbd81b5ce65f2e99c6e243ad03
links:
  - to: snapog-landing-pages
    relation: uses
    description: The landing page's waitlist form posts here.
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

Cloudflare Pages Function for POST /api/waitlist capturing email signups. Validates email, deduplicates against the WAITLIST KV namespace (email:<address> key), stores JSON with source/IP/UA/timestamp, returns 503 if the binding is missing so the client falls back to Formspree/mailto. Normalizes emails to lowercase, truncates source/UA, sets cache-control: no-store, and returns deduped:true on duplicates.

## Related

- uses [[snapog-landing-pages]] — The landing page's waitlist form posts here.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
