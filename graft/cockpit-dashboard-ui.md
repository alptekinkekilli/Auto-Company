---
name: Cockpit dashboard UI
slug: cockpit-dashboard-ui
type: system
sources:
  - path: dashboard/app.js
    hash: 96f503ea5d6c678db76dbf8202fa8d454492bc3d403fef01f433b8a6b52f1c44
sources_digest: 6615bd5ca9dec72f7ec6d40af96a5864ec9fca878a10df4898794f2497b83adf
links:
  - to: cockpit-dashboard-server
    relation: uses
    description: >-
      Calls /api/status, /api/hold, /api/directive, /api/ideas, /api/tool-usage,
      /api/analysis REST endpoints served by server.py.
generator:
  version: 1
covers:
  - symbol: escapeHtml
    kind: function
    at: 'dashboard/app.js:L85-L92'
  - symbol: renderInlineMarkdown
    kind: function
    at: 'dashboard/app.js:L94-L101'
  - symbol: renderMarkdown
    kind: function
    at: 'dashboard/app.js:L103-L185'
  - symbol: closeParagraph
    kind: function
    at: 'dashboard/app.js:L110-L115'
  - symbol: closeList
    kind: function
    at: 'dashboard/app.js:L116-L121'
  - symbol: classForState
    kind: function
    at: 'dashboard/app.js:L187-L209'
  - symbol: applyCardState
    kind: function
    at: 'dashboard/app.js:L211-L214'
  - symbol: formatTime
    kind: function
    at: 'dashboard/app.js:L216-L222'
  - symbol: renderStateList
    kind: function
    at: 'dashboard/app.js:L224-L251'
  - symbol: ladder
    kind: function
    at: 'dashboard/app.js:L230-L230'
  - symbol: fetchStatus
    kind: function
    at: 'dashboard/app.js:L253-L313'
  - symbol: renderCost
    kind: function
    at: 'dashboard/app.js:L315-L351'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L316-L316'
  - symbol: renderCcusage
    kind: function
    at: 'dashboard/app.js:L353-L373'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L355-L355'
  - symbol: renderHold
    kind: function
    at: 'dashboard/app.js:L379-L389'
  - symbol: setHold
    kind: function
    at: 'dashboard/app.js:L391-L421'
  - symbol: renderDirective
    kind: function
    at: 'dashboard/app.js:L423-L438'
  - symbol: submitDirective
    kind: function
    at: 'dashboard/app.js:L440-L483'
  - symbol: send
    kind: function
    at: 'dashboard/app.js:L451-L456'
  - symbol: renderSettings
    kind: function
    at: 'dashboard/app.js:L485-L505'
  - symbol: gatherSettings
    kind: function
    at: 'dashboard/app.js:L507-L514'
  - symbol: loadIdeas
    kind: function
    at: 'dashboard/app.js:L517-L537'
  - symbol: loadToolUsage
    kind: function
    at: 'dashboard/app.js:L540-L575'
  - symbol: loadAnalysis
    kind: function
    at: 'dashboard/app.js:L579-L603'
  - symbol: renderAnalystTrigger
    kind: function
    at: 'dashboard/app.js:L607-L620'
  - symbol: runAnalystNow
    kind: function
    at: 'dashboard/app.js:L622-L639'
  - symbol: extractDirective
    kind: function
    at: 'dashboard/app.js:L645-L657'
  - symbol: copyToBtn
    kind: function
    at: 'dashboard/app.js:L659-L667'
  - symbol: loadDirectiveTemplates
    kind: function
    at: 'dashboard/app.js:L681-L713'
  - symbol: loadSettings
    kind: function
    at: 'dashboard/app.js:L716-L724'
  - symbol: saveSettings
    kind: function
    at: 'dashboard/app.js:L726-L755'
  - symbol: setWakeAvailability
    kind: function
    at: 'dashboard/app.js:L761-L768'
  - symbol: wakeLoop
    kind: function
    at: 'dashboard/app.js:L770-L787'
  - symbol: resetAutoTimer
    kind: function
    at: 'dashboard/app.js:L790-L803'
  - symbol: notifiedIds
    kind: function
    at: 'dashboard/app.js:L879-L886'
  - symbol: rememberNotified
    kind: function
    at: 'dashboard/app.js:L888-L895'
  - symbol: renderNotifyButton
    kind: function
    at: 'dashboard/app.js:L897-L915'
  - symbol: announceNewRequests
    kind: function
    at: 'dashboard/app.js:L917-L937'
  - symbol: opreqPanelBusy
    kind: function
    at: 'dashboard/app.js:L945-L952'
  - symbol: renderOperatorRequests
    kind: function
    at: 'dashboard/app.js:L954-L1013'
  - symbol: submitDecision
    kind: function
    at: 'dashboard/app.js:L1015-L1054'
  - symbol: loadOperatorRequests
    kind: function
    at: 'dashboard/app.js:L1056-L1063'
---
<!-- context:generated:start -->
## Summary

Client-side single-page controller for the cockpit dashboard: polls /api/status, renders live system state, cost metrics, hold/release, directive submission, settings, ideas, tool-usage, and analyst output. No external libraries; safe HTML/markdown rendering; several load functions only set loaded flag on success to avoid transient failures sticking.

## Related

- uses [[cockpit-dashboard-server]] — Calls /api/status, /api/hold, /api/directive, /api/ideas, /api/tool-usage, /api/analysis REST endpoints served by server.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
