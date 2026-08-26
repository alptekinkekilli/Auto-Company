---
name: SnapOG OG Rendering
slug: snapog-og-rendering
type: system
sources:
  - path: projects/_archive/snapog/src/og/render.ts
    hash: c74a09fcf98afae74090c3b72b8b4c7f84252e7f0aca090d1418352cd48d8094
  - path: projects/_archive/snapog/src/og/templates.ts
    hash: bfc8c9e61038224564b61c55c627b2d86d9ba2514dd47f64a717e94f0be8b810
sources_digest: 33ae7a75e47eef85db34a1438baacae47da77dae7fb7876ade82ebe4c7f21f57
links:
  - to: snapog-worker
    relation: implements
    description: Provides the image generation and cache-key logic the worker calls.
generator:
  version: 1
covers:
  - symbol: generateOGImage
    kind: function
    at: 'projects/_archive/snapog/src/og/render.ts:L11-L23'
  - symbol: buildCacheKey
    kind: function
    at: 'projects/_archive/snapog/src/og/render.ts:L26-L37'
  - symbol: StyleObject
    kind: type
    at: 'projects/_archive/snapog/src/og/templates.ts:L6-L6'
  - symbol: VNode
    kind: type
    at: 'projects/_archive/snapog/src/og/templates.ts:L8-L15'
  - symbol: AccentBar
    kind: function
    at: 'projects/_archive/snapog/src/og/templates.ts:L18-L33'
  - symbol: Header
    kind: function
    at: 'projects/_archive/snapog/src/og/templates.ts:L36-L83'
  - symbol: Footer
    kind: function
    at: 'projects/_archive/snapog/src/og/templates.ts:L86-L133'
  - symbol: defaultTemplate
    kind: function
    at: 'projects/_archive/snapog/src/og/templates.ts:L136-L202'
  - symbol: blogTemplate
    kind: function
    at: 'projects/_archive/snapog/src/og/templates.ts:L205-L286'
  - symbol: articleTemplate
    kind: function
    at: 'projects/_archive/snapog/src/og/templates.ts:L289-L461'
  - symbol: buildElement
    kind: function
    at: 'projects/_archive/snapog/src/og/templates.ts:L463-L472'
---
<!-- context:generated:start -->
## Summary

OG image generation module: render.ts builds the ImageResponse at fixed 1200x630 and produces a deterministic SHA-256 cache key by JSON-stringifying params (sorted keys, watermark merged) so identical inputs always yield the same key; templates.ts builds plain VNode trees (default/blog/article) with theme palettes, dynamic font sizing, and a watermark toggle. crypto.subtle requires a secure context, so cache-key only works in Workers/HTTPS.

## Related

- implements [[snapog-worker]] — Provides the image generation and cache-key logic the worker calls.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
