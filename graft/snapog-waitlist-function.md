---
name: SnapOG Waitlist Function
slug: snapog-waitlist-function
type: file
sources: []
sources_digest: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
links: []
generator:
  version: 1
covers: []
---
<!-- context:generated:start -->
## Summary

Cloudflare Pages Function for POST /api/waitlist, validating and deduplicating email signups against a KV namespace. Normalizes emails to lowercase, truncates source/user-agent, uses email:<address> keys, returns 503 if the binding is missing (client falls back to Formspree/mailto), and sets cache-control: no-store.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
