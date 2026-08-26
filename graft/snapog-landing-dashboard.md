---
name: SnapOG Landing & Dashboard
slug: snapog-landing-dashboard
type: file
sources:
  - path: projects/_archive/snapog/src/dashboard/pages.ts
    hash: 6a33d1b6152ee8ea3ee6f5617105ce757c915627156072dd9cb1f3b78e32b4af
sources_digest: aa49b78a6522f0383edeedf2bbb936457599ccfbd81b5ce65f2e99c6e243ad03
links:
  - to: snapog-service
    relation: part_of
    description: Renders the / and /dashboard routes.
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

Server-side HTML template module for the public landing page and dashboard, implementing the 'Carbon Terminal' aesthetic with template literals and no client-side framework. Threads the host argument into code examples and meta tags to build absolute URLs, and embeds a live OG image preview hitting the actual /og endpoint plus hardcoded pricing tiers.

## Related

- part of [[snapog-service]] — Renders the / and /dashboard routes.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
