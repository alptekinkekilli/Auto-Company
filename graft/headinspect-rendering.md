---
name: HeadInspect Rendering
slug: headinspect-rendering
type: file
sources:
  - path: projects/headinspect/src/render.ts
    hash: 3792b2bd4004ee751d9ae6647d0fc58d9708ef758ad6bfda6beb0a4314bd8883
sources_digest: c1fd5ab5035979e15031a703d3af275a0f68bfd9fa619bad6929d3e848f8e2d2
links:
  - to: headinspect-worker
    relation: implements
    description: Renders the HTML pages and badge.svg.
generator:
  version: 1
covers:
  - symbol: escapeHtml
    kind: function
    at: 'projects/headinspect/src/render.ts:L16-L23'
  - symbol: badgeColor
    kind: function
    at: 'projects/headinspect/src/render.ts:L27-L36'
  - symbol: textWidth
    kind: function
    at: 'projects/headinspect/src/render.ts:L39-L41'
  - symbol: renderBadge
    kind: function
    at: 'projects/headinspect/src/render.ts:L46-L79'
  - symbol: renderEmbedBlock
    kind: function
    at: 'projects/headinspect/src/render.ts:L81-L94'
  - symbol: renderReport
    kind: function
    at: 'projects/headinspect/src/render.ts:L96-L137'
  - symbol: hostOf
    kind: function
    at: 'projects/headinspect/src/render.ts:L139-L141'
  - symbol: socialMeta
    kind: function
    at: 'projects/headinspect/src/render.ts:L143-L176'
  - symbol: renderPage
    kind: function
    at: 'projects/headinspect/src/render.ts:L178-L242'
---
<!-- context:generated:start -->
## Summary

Single-template HTML renderer producing all server-rendered pages and SVG badges with no client framework and inline CSS. renderPage builds the full document; renderBadge generates a shields.io-flavoured flat SVG badge. Rough 11px Verdana text-width heuristic with textLength scaling for stable badge rendering across font substitutions; CSS variables for light/dark via prefers-color-scheme; hardcoded 400-char truncation on header values.

## Related

- implements [[headinspect-worker]] — Renders the HTML pages and badge.svg.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
