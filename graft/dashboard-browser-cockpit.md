---
name: Dashboard browser cockpit
slug: dashboard-browser-cockpit
type: system
sources:
  - path: dashboard/app.js
    hash: d53598929d12a8200a66b5a1f67e62fa92cb2ada0adecf4fec62d188c86e0347
sources_digest: 32f4aa1cab1e68b6c3fc357dff48e76a4440dac86230d377e716d816daecbd37
links:
  - to: dashboard-server
    relation: uses
    description: >-
      Polls /api/status and posts directive/settings/operator decisions to the
      server endpoints.
generator:
  version: 1
covers:
  - symbol: escapeHtml
    kind: function
    at: 'dashboard/app.js:L89-L96'
  - symbol: renderInlineMarkdown
    kind: function
    at: 'dashboard/app.js:L98-L105'
  - symbol: renderMarkdown
    kind: function
    at: 'dashboard/app.js:L107-L189'
  - symbol: closeParagraph
    kind: function
    at: 'dashboard/app.js:L114-L119'
  - symbol: closeList
    kind: function
    at: 'dashboard/app.js:L120-L125'
  - symbol: classForState
    kind: function
    at: 'dashboard/app.js:L191-L213'
  - symbol: applyCardState
    kind: function
    at: 'dashboard/app.js:L215-L218'
  - symbol: formatTime
    kind: function
    at: 'dashboard/app.js:L220-L226'
  - symbol: renderStateList
    kind: function
    at: 'dashboard/app.js:L228-L255'
  - symbol: ladder
    kind: function
    at: 'dashboard/app.js:L234-L234'
  - symbol: fetchStatus
    kind: function
    at: 'dashboard/app.js:L257-L317'
  - symbol: renderCost
    kind: function
    at: 'dashboard/app.js:L319-L362'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L320-L320'
  - symbol: renderCcusage
    kind: function
    at: 'dashboard/app.js:L364-L384'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L366-L366'
  - symbol: renderHold
    kind: function
    at: 'dashboard/app.js:L390-L400'
  - symbol: setHold
    kind: function
    at: 'dashboard/app.js:L402-L432'
  - symbol: renderDirective
    kind: function
    at: 'dashboard/app.js:L434-L449'
  - symbol: submitDirective
    kind: function
    at: 'dashboard/app.js:L451-L494'
  - symbol: send
    kind: function
    at: 'dashboard/app.js:L462-L467'
  - symbol: renderSettings
    kind: function
    at: 'dashboard/app.js:L496-L516'
  - symbol: gatherSettings
    kind: function
    at: 'dashboard/app.js:L518-L525'
  - symbol: loadIdeas
    kind: function
    at: 'dashboard/app.js:L528-L548'
  - symbol: loadToolUsage
    kind: function
    at: 'dashboard/app.js:L551-L586'
  - symbol: loadAnalysis
    kind: function
    at: 'dashboard/app.js:L590-L614'
  - symbol: renderAnalystTrigger
    kind: function
    at: 'dashboard/app.js:L618-L631'
  - symbol: runAnalystNow
    kind: function
    at: 'dashboard/app.js:L633-L650'
  - symbol: extractDirective
    kind: function
    at: 'dashboard/app.js:L656-L668'
  - symbol: copyToBtn
    kind: function
    at: 'dashboard/app.js:L670-L678'
  - symbol: loadDirectiveTemplates
    kind: function
    at: 'dashboard/app.js:L692-L724'
  - symbol: loadSettings
    kind: function
    at: 'dashboard/app.js:L727-L735'
  - symbol: saveSettings
    kind: function
    at: 'dashboard/app.js:L737-L766'
  - symbol: setWakeAvailability
    kind: function
    at: 'dashboard/app.js:L772-L779'
  - symbol: wakeLoop
    kind: function
    at: 'dashboard/app.js:L781-L798'
  - symbol: resetAutoTimer
    kind: function
    at: 'dashboard/app.js:L801-L814'
  - symbol: notifiedIds
    kind: function
    at: 'dashboard/app.js:L890-L897'
  - symbol: rememberNotified
    kind: function
    at: 'dashboard/app.js:L899-L906'
  - symbol: renderNotifyButton
    kind: function
    at: 'dashboard/app.js:L908-L926'
  - symbol: announceNewRequests
    kind: function
    at: 'dashboard/app.js:L928-L948'
  - symbol: opreqPanelBusy
    kind: function
    at: 'dashboard/app.js:L956-L963'
  - symbol: renderOperatorRequests
    kind: function
    at: 'dashboard/app.js:L965-L1024'
  - symbol: submitDecision
    kind: function
    at: 'dashboard/app.js:L1026-L1065'
  - symbol: loadOperatorRequests
    kind: function
    at: 'dashboard/app.js:L1067-L1074'
---
<!-- context:generated:start -->
## Summary

The vanilla-JS single-page dashboard that polls /api/status and renders live state for guardian, daemon, loop, and autostart services, plus cost, directive, hold, and consensus panels. Implements a custom markdown renderer with HTML escaping, colors service cards by health, and handles Hold/Release (replacing the no-op Start/Stop buttons), directive submission with an allowPending supersede flow, and settings editing. Loads auxiliary panels lazily with retry-on-failure semantics.

## Related

- uses [[dashboard-server]] — Polls /api/status and posts directive/settings/operator decisions to the server endpoints.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
