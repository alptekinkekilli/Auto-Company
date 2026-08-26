---
name: Cockpit Dashboard
slug: cockpit-dashboard
type: system
sources:
  - path: dashboard/app.js
    hash: 1a974b1c1d72cf714de69954e840a6335990788860f9442ad1e61fcf6f041ca8
  - path: dashboard/sentry_client.py
    hash: 96977bb6701f18064edb69c783e53bdb73c930c8ddadcd1caf47583b42700df4
sources_digest: f7cffd86cee6a866334be6fc13e2b3724150ee08680c1996bf52b88ccc7091f6
links:
  - to: cockpit-dashboard-server
    relation: uses
    description: >-
      app.js polls /api/status, /api/hold, /api/directive, /api/ideas,
      /api/tool-usage served by server.py; sentry_client.py is imported by
      server.py for error reporting.
generator:
  version: 1
covers:
  - symbol: escapeHtml
    kind: function
    at: 'dashboard/app.js:L92-L99'
  - symbol: renderInlineMarkdown
    kind: function
    at: 'dashboard/app.js:L101-L108'
  - symbol: renderMarkdown
    kind: function
    at: 'dashboard/app.js:L110-L192'
  - symbol: closeParagraph
    kind: function
    at: 'dashboard/app.js:L117-L122'
  - symbol: closeList
    kind: function
    at: 'dashboard/app.js:L123-L128'
  - symbol: classForState
    kind: function
    at: 'dashboard/app.js:L194-L216'
  - symbol: applyCardState
    kind: function
    at: 'dashboard/app.js:L218-L221'
  - symbol: renderGraft
    kind: function
    at: 'dashboard/app.js:L223-L246'
  - symbol: formatTime
    kind: function
    at: 'dashboard/app.js:L248-L254'
  - symbol: renderStateList
    kind: function
    at: 'dashboard/app.js:L256-L285'
  - symbol: ladder
    kind: function
    at: 'dashboard/app.js:L262-L262'
  - symbol: fetchStatus
    kind: function
    at: 'dashboard/app.js:L287-L348'
  - symbol: renderCost
    kind: function
    at: 'dashboard/app.js:L350-L398'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L351-L351'
  - symbol: renderCcusage
    kind: function
    at: 'dashboard/app.js:L400-L420'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L402-L402'
  - symbol: renderHold
    kind: function
    at: 'dashboard/app.js:L426-L436'
  - symbol: setHold
    kind: function
    at: 'dashboard/app.js:L438-L468'
  - symbol: renderDirective
    kind: function
    at: 'dashboard/app.js:L470-L485'
  - symbol: submitDirective
    kind: function
    at: 'dashboard/app.js:L487-L530'
  - symbol: send
    kind: function
    at: 'dashboard/app.js:L498-L503'
  - symbol: renderSettings
    kind: function
    at: 'dashboard/app.js:L532-L552'
  - symbol: gatherSettings
    kind: function
    at: 'dashboard/app.js:L554-L561'
  - symbol: loadIdeas
    kind: function
    at: 'dashboard/app.js:L564-L584'
  - symbol: loadToolUsage
    kind: function
    at: 'dashboard/app.js:L587-L622'
  - symbol: loadAnalysis
    kind: function
    at: 'dashboard/app.js:L626-L650'
  - symbol: renderAnalystTrigger
    kind: function
    at: 'dashboard/app.js:L654-L667'
  - symbol: runAnalystNow
    kind: function
    at: 'dashboard/app.js:L669-L686'
  - symbol: extractDirective
    kind: function
    at: 'dashboard/app.js:L692-L704'
  - symbol: copyToBtn
    kind: function
    at: 'dashboard/app.js:L706-L714'
  - symbol: loadDirectiveTemplates
    kind: function
    at: 'dashboard/app.js:L728-L760'
  - symbol: loadSettings
    kind: function
    at: 'dashboard/app.js:L763-L771'
  - symbol: saveSettings
    kind: function
    at: 'dashboard/app.js:L773-L802'
  - symbol: setWakeAvailability
    kind: function
    at: 'dashboard/app.js:L808-L815'
  - symbol: wakeLoop
    kind: function
    at: 'dashboard/app.js:L817-L834'
  - symbol: resetAutoTimer
    kind: function
    at: 'dashboard/app.js:L837-L850'
  - symbol: notifiedIds
    kind: function
    at: 'dashboard/app.js:L926-L933'
  - symbol: rememberNotified
    kind: function
    at: 'dashboard/app.js:L935-L942'
  - symbol: renderNotifyButton
    kind: function
    at: 'dashboard/app.js:L944-L962'
  - symbol: announceNewRequests
    kind: function
    at: 'dashboard/app.js:L964-L984'
  - symbol: opreqPanelBusy
    kind: function
    at: 'dashboard/app.js:L992-L999'
  - symbol: renderOperatorRequests
    kind: function
    at: 'dashboard/app.js:L1001-L1060'
  - symbol: submitDecision
    kind: function
    at: 'dashboard/app.js:L1062-L1101'
  - symbol: loadOperatorRequests
    kind: function
    at: 'dashboard/app.js:L1103-L1110'
  - symbol: _parse_dsn
    kind: function
    at: 'dashboard/sentry_client.py:L33-L43'
  - symbol: capture_exception
    kind: function
    at: 'dashboard/sentry_client.py:L49-L102'
---
<!-- context:generated:start -->
## Summary

Browser-side SPA controller plus its stdlib-only Sentry reporter. Polls /api/status on a timer and renders live state cards, cost/usage panels, directive editor, settings form, and log/consensus views. All state comes from backend REST endpoints; no external libraries. The consensus panel refuses to overwrite while the operator is reading the full file; ccusage fails open; tool-usage is a real table because the Rajdhani font is proportional.

## Related

- uses [[cockpit-dashboard-server]] — app.js polls /api/status, /api/hold, /api/directive, /api/ideas, /api/tool-usage served by server.py; sentry_client.py is imported by server.py for error reporting.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
