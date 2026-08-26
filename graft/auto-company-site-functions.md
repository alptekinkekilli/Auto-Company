---
name: Auto-Company Site Functions
slug: auto-company-site-functions
type: system
sources:
  - path: projects/auto-company-site/functions/listeden-cik.js
    hash: 7da883b7faec5b5065d071608172ca1d8effa6a3e255bc1cd658181000936229
  - path: projects/auto-company-site/functions/randevu.js
    hash: 680f4267bf50111c0d6d05e9068a837e04e46dc3a7cac7d549eb3e7a35c708bb
sources_digest: d765296cba06e0858b94642f9c57598b0a01dbdbf1099116ab94c5ce24458b9c
links: []
generator:
  version: 1
covers:
  - symbol: onRequestGet
    kind: function
    at: 'projects/auto-company-site/functions/listeden-cik.js:L19-L46'
  - symbol: errorPage
    kind: function
    at: 'projects/auto-company-site/functions/listeden-cik.js:L48-L59'
  - symbol: onRequestGet
    kind: function
    at: 'projects/auto-company-site/functions/randevu.js:L17-L34'
  - symbol: page
    kind: function
    at: 'projects/auto-company-site/functions/randevu.js:L36-L47'
---
<!-- context:generated:start -->
## Summary

Cloudflare Pages Functions for the auto-company marketing site: /randevu issues a 302 redirect to the operator's Google Calendar page (no booking logic — slot management, timezone, cancellation delegated to Google Calendar), and /listeden-cik is a branded presentation-layer proxy forwarding to the Twilio comms service unsubscribe endpoint, deliberately with no local suppression store so the upstream remains the single source of truth. Both preserve trust in cold B2B outreach by keeping links on the company's own domain, return Turkish fallback pages on failure (never a guessed redirect or false success), and set no-store/no-referrer headers.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
