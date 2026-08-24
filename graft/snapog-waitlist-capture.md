---
name: SnapOG waitlist capture
slug: snapog-waitlist-capture
type: system
sources:
  - path: projects/_archive/snapog-landing/functions/api/waitlist.ts
    hash: 49b5d66187a49f386d4bee50c1c01042d595e5ebbd5b27c061f1fba4cffeefa0
sources_digest: 2eab55af564b0f608bf8be780ff3a47c7384bb204d191cb437072802784c073f
links: []
generator:
  version: 1
covers:
  - symbol: Env
    kind: interface
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L12-L14'
  - symbol: Body
    kind: interface
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L16-L20'
  - symbol: onRequestPost
    kind: function
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L24-L62'
  - symbol: json
    kind: function
    at: 'projects/_archive/snapog-landing/functions/api/waitlist.ts:L64-L72'
---
<!-- context:generated:start -->
## Summary

A Cloudflare Pages Function for POST /api/waitlist that validates, deduplicates against a KV namespace, and stores email signups, returning a 503 if the binding is missing so the client falls back to Formspree/mailto. Normalizes emails to lowercase, truncates source/user-agent, uses email:<address> keys for dedup, and sets cache-control: no-store.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
