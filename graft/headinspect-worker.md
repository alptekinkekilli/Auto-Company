---
name: HeadInspect Worker
slug: headinspect-worker
type: system
sources:
  - path: projects/headinspect/src/index.ts
    hash: 2c4962e89d06e9fb5bf12aad7cdd08634974a4f57f59cceaa6dca9c98e771499
sources_digest: 1651f2a75c6cc66090673b59fbb99aa23cb05a94ef661e0b49dea46746359d52
links:
  - to: headinspect-inspection-logic
    relation: uses
    description: >-
      Delegates header categorization and grading to categorizeHeaders/grade
      from ./inspect.
  - to: headinspect-renderer
    relation: uses
    description: >-
      Delegates page and badge rendering to renderPage/renderBadge from
      ./render.
generator:
  version: 1
covers:
  - symbol: fetch
    kind: method
    at: 'projects/headinspect/src/index.ts:L24-L83'
  - symbol: TargetOk
    kind: type
    at: 'projects/headinspect/src/index.ts:L88-L88'
  - symbol: TargetErr
    kind: type
    at: 'projects/headinspect/src/index.ts:L89-L89'
  - symbol: extractTarget
    kind: function
    at: 'projects/headinspect/src/index.ts:L91-L104'
  - symbol: validateUrl
    kind: function
    at: 'projects/headinspect/src/index.ts:L108-L119'
  - symbol: isBlockedHost
    kind: function
    at: 'projects/headinspect/src/index.ts:L121-L147'
  - symbol: InspectOk
    kind: type
    at: 'projects/headinspect/src/index.ts:L151-L151'
  - symbol: InspectErr
    kind: type
    at: 'projects/headinspect/src/index.ts:L152-L152'
  - symbol: inspect
    kind: function
    at: 'projects/headinspect/src/index.ts:L154-L229'
  - symbol: consume
    kind: function
    at: 'projects/headinspect/src/index.ts:L232-L246'
  - symbol: json
    kind: function
    at: 'projects/headinspect/src/index.ts:L250-L259'
  - symbol: html
    kind: function
    at: 'projects/headinspect/src/index.ts:L261-L271'
  - symbol: svg
    kind: function
    at: 'projects/headinspect/src/index.ts:L275-L284'
---
<!-- context:generated:start -->
## Summary

Cloudflare Worker exposing an HTTP API and HTML UI that fetches a user-supplied URL and reports on its response headers. Routes / (HTML report or JSON), /api/inspect, /health, /badge.svg. Enforces strict SSRF protections via validateUrl/isBlockedHost (rejects non-HTTPS, localhost, private IP ranges, cloud metadata endpoints), follows up to five redirects manually, drains bodies to free sockets, 10-second AbortController timeout. Badge always returns HTTP 200 with edge caching so broken embeds never render as broken images.

## Related

- uses [[headinspect-inspection-logic]] — Delegates header categorization and grading to categorizeHeaders/grade from ./inspect.
- uses [[headinspect-renderer]] — Delegates page and badge rendering to renderPage/renderBadge from ./render.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
