---
name: Cockpit Dashboard
slug: cockpit-dashboard
type: system
sources:
  - path: dashboard/app.js
    hash: f12257a8f9a08f27b890003b8139742f7ab86e0e5279c03f494f9a2aee8ec4ae
  - path: dashboard/sentry_client.py
    hash: 96977bb6701f18064edb69c783e53bdb73c930c8ddadcd1caf47583b42700df4
  - path: dashboard/server.py
    hash: 70cf0bcbe6dc4a6d7eefbe16eb758cb028604ef507c20bb090612ce803b21083
sources_digest: 301ea95057cc663d6370439872af0d0ddbddd75a658b7cf5da46fb05ca84b07c
links:
  - to: autonomous-loop
    relation: uses
    description: >-
      The dashboard's hold/release is the only real loop control; it
      reads/writes loop state files and the auto-loop.log tail.
  - to: directive-writer
    relation: uses
    description: >-
      server.py routes all directive writes through directive_writer.py to
      enforce the PENDING-clobber and body-immutability rules.
  - to: sentry-reporter
    relation: uses
    description: server.py reports errors via sentry_client.capture_exception.
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
    at: 'dashboard/app.js:L228-L257'
  - symbol: ladder
    kind: function
    at: 'dashboard/app.js:L234-L234'
  - symbol: fetchStatus
    kind: function
    at: 'dashboard/app.js:L259-L319'
  - symbol: renderCost
    kind: function
    at: 'dashboard/app.js:L321-L369'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L322-L322'
  - symbol: renderCcusage
    kind: function
    at: 'dashboard/app.js:L371-L391'
  - symbol: usd
    kind: function
    at: 'dashboard/app.js:L373-L373'
  - symbol: renderHold
    kind: function
    at: 'dashboard/app.js:L397-L407'
  - symbol: setHold
    kind: function
    at: 'dashboard/app.js:L409-L439'
  - symbol: renderDirective
    kind: function
    at: 'dashboard/app.js:L441-L456'
  - symbol: submitDirective
    kind: function
    at: 'dashboard/app.js:L458-L501'
  - symbol: send
    kind: function
    at: 'dashboard/app.js:L469-L474'
  - symbol: renderSettings
    kind: function
    at: 'dashboard/app.js:L503-L523'
  - symbol: gatherSettings
    kind: function
    at: 'dashboard/app.js:L525-L532'
  - symbol: loadIdeas
    kind: function
    at: 'dashboard/app.js:L535-L555'
  - symbol: loadToolUsage
    kind: function
    at: 'dashboard/app.js:L558-L593'
  - symbol: loadAnalysis
    kind: function
    at: 'dashboard/app.js:L597-L621'
  - symbol: renderAnalystTrigger
    kind: function
    at: 'dashboard/app.js:L625-L638'
  - symbol: runAnalystNow
    kind: function
    at: 'dashboard/app.js:L640-L657'
  - symbol: extractDirective
    kind: function
    at: 'dashboard/app.js:L663-L675'
  - symbol: copyToBtn
    kind: function
    at: 'dashboard/app.js:L677-L685'
  - symbol: loadDirectiveTemplates
    kind: function
    at: 'dashboard/app.js:L699-L731'
  - symbol: loadSettings
    kind: function
    at: 'dashboard/app.js:L734-L742'
  - symbol: saveSettings
    kind: function
    at: 'dashboard/app.js:L744-L773'
  - symbol: setWakeAvailability
    kind: function
    at: 'dashboard/app.js:L779-L786'
  - symbol: wakeLoop
    kind: function
    at: 'dashboard/app.js:L788-L805'
  - symbol: resetAutoTimer
    kind: function
    at: 'dashboard/app.js:L808-L821'
  - symbol: notifiedIds
    kind: function
    at: 'dashboard/app.js:L897-L904'
  - symbol: rememberNotified
    kind: function
    at: 'dashboard/app.js:L906-L913'
  - symbol: renderNotifyButton
    kind: function
    at: 'dashboard/app.js:L915-L933'
  - symbol: announceNewRequests
    kind: function
    at: 'dashboard/app.js:L935-L955'
  - symbol: opreqPanelBusy
    kind: function
    at: 'dashboard/app.js:L963-L970'
  - symbol: renderOperatorRequests
    kind: function
    at: 'dashboard/app.js:L972-L1031'
  - symbol: submitDecision
    kind: function
    at: 'dashboard/app.js:L1033-L1072'
  - symbol: loadOperatorRequests
    kind: function
    at: 'dashboard/app.js:L1074-L1081'
  - symbol: _parse_dsn
    kind: function
    at: 'dashboard/sentry_client.py:L33-L43'
  - symbol: capture_exception
    kind: function
    at: 'dashboard/sentry_client.py:L49-L102'
  - symbol: ps_quote
    kind: function
    at: 'dashboard/server.py:L123-L124'
  - symbol: detect_host_kind
    kind: function
    at: 'dashboard/server.py:L127-L137'
  - symbol: run_powershell_script
    kind: function
    at: 'dashboard/server.py:L140-L184'
  - symbol: run_shell_script
    kind: function
    at: 'dashboard/server.py:L187-L217'
  - symbol: get_host_profile
    kind: function
    at: 'dashboard/server.py:L220-L253'
  - symbol: read_text_file
    kind: function
    at: 'dashboard/server.py:L256-L270'
  - symbol: read_text_file_tail
    kind: function
    at: 'dashboard/server.py:L273-L305'
  - symbol: read_directive
    kind: function
    at: 'dashboard/server.py:L315-L347'
  - symbol: _section
    kind: function
    at: 'dashboard/server.py:L326-L337'
  - symbol: DirectiveRefused
    kind: class
    at: 'dashboard/server.py:L350-L351'
  - symbol: write_directive
    kind: function
    at: 'dashboard/server.py:L354-L397'
  - symbol: parse_proposed_authorization
    kind: function
    at: 'dashboard/server.py:L426-L435'
  - symbol: read_operator_requests
    kind: function
    at: 'dashboard/server.py:L438-L473'
  - symbol: _decisions_audit
    kind: function
    at: 'dashboard/server.py:L476-L483'
  - symbol: write_operator_decision
    kind: function
    at: 'dashboard/server.py:L486-L572'
  - symbol: _parse_env_file
    kind: function
    at: 'dashboard/server.py:L575-L587'
  - symbol: read_ideas
    kind: function
    at: 'dashboard/server.py:L590-L608'
  - symbol: read_tool_usage
    kind: function
    at: 'dashboard/server.py:L611-L648'
  - symbol: read_analysis
    kind: function
    at: 'dashboard/server.py:L651-L669'
  - symbol: analyst_trigger_state
    kind: function
    at: 'dashboard/server.py:L672-L679'
  - symbol: analyst_run_now
    kind: function
    at: 'dashboard/server.py:L682-L708'
  - symbol: read_directive_templates
    kind: function
    at: 'dashboard/server.py:L726-L733'
  - symbol: read_settings
    kind: function
    at: 'dashboard/server.py:L736-L778'
  - symbol: write_settings
    kind: function
    at: 'dashboard/server.py:L781-L827'
  - symbol: _proc_cmdline
    kind: function
    at: 'dashboard/server.py:L830-L835'
  - symbol: _proc_ppid
    kind: function
    at: 'dashboard/server.py:L838-L845'
  - symbol: read_hold
    kind: function
    at: 'dashboard/server.py:L852-L875'
  - symbol: set_hold
    kind: function
    at: 'dashboard/server.py:L878-L915'
  - symbol: wake_loop
    kind: function
    at: 'dashboard/server.py:L918-L976'
  - symbol: trigger_redeploy
    kind: function
    at: 'dashboard/server.py:L979-L1015'
  - symbol: _week_start_epoch
    kind: function
    at: 'dashboard/server.py:L1031-L1038'
  - symbol: _ccusage_compute
    kind: function
    at: 'dashboard/server.py:L1041-L1096'
  - symbol: _run
    kind: function
    at: 'dashboard/server.py:L1047-L1055'
  - symbol: _is_codex
    kind: function
    at: 'dashboard/server.py:L1070-L1072'
  - symbol: read_ccusage
    kind: function
    at: 'dashboard/server.py:L1099-L1119'
  - symbol: _bg
    kind: function
    at: 'dashboard/server.py:L1111-L1116'
  - symbol: read_engine_runtime
    kind: function
    at: 'dashboard/server.py:L1122-L1219'
  - symbol: _window_cutoff_epoch
    kind: function
    at: 'dashboard/server.py:L1222-L1250'
  - symbol: read_cost_summary
    kind: function
    at: 'dashboard/server.py:L1253-L1384'
  - symbol: _last_budget_gate
    kind: function
    at: 'dashboard/server.py:L1387-L1395'
  - symbol: read_tail
    kind: function
    at: 'dashboard/server.py:L1398-L1405'
  - symbol: parse_sections
    kind: function
    at: 'dashboard/server.py:L1408-L1423'
  - symbol: parse_int
    kind: function
    at: 'dashboard/server.py:L1426-L1430'
  - symbol: parse_positive_int
    kind: function
    at: 'dashboard/server.py:L1433-L1438'
  - symbol: parse_key_values
    kind: function
    at: 'dashboard/server.py:L1441-L1448'
  - symbol: blank_parsed
    kind: function
    at: 'dashboard/server.py:L1451-L1475'
  - symbol: parse_windows_status_output
    kind: function
    at: 'dashboard/server.py:L1478-L1560'
  - symbol: parse_macos_status_output
    kind: function
    at: 'dashboard/server.py:L1563-L1599'
  - symbol: read_state_file_pairs
    kind: function
    at: 'dashboard/server.py:L1602-L1610'
  - symbol: run_status_command
    kind: function
    at: 'dashboard/server.py:L1613-L1616'
  - symbol: run_dashboard_action
    kind: function
    at: 'dashboard/server.py:L1619-L1631'
  - symbol: parse_status_output
    kind: function
    at: 'dashboard/server.py:L1634-L1636'
  - symbol: gather_status_payload
    kind: function
    at: 'dashboard/server.py:L1639-L1658'
  - symbol: DashboardHandler
    kind: class
    at: 'dashboard/server.py:L1661-L1966'
  - symbol: _json
    kind: method
    at: 'dashboard/server.py:L1662-L1669'
  - symbol: _text
    kind: method
    at: 'dashboard/server.py:L1671-L1680'
  - symbol: _serve_file
    kind: method
    at: 'dashboard/server.py:L1682-L1686'
  - symbol: do_GET
    kind: method
    at: 'dashboard/server.py:L1688-L1693'
  - symbol: _do_GET
    kind: method
    at: 'dashboard/server.py:L1695-L1761'
  - symbol: _read_body
    kind: method
    at: 'dashboard/server.py:L1763-L1770'
  - symbol: do_POST
    kind: method
    at: 'dashboard/server.py:L1772-L1777'
  - symbol: _do_POST
    kind: method
    at: 'dashboard/server.py:L1779-L1842'
  - symbol: _handle_operator_decision
    kind: method
    at: 'dashboard/server.py:L1844-L1884'
  - symbol: _handle_directive
    kind: method
    at: 'dashboard/server.py:L1886-L1932'
  - symbol: _handle_settings
    kind: method
    at: 'dashboard/server.py:L1934-L1963'
  - symbol: log_message
    kind: method
    at: 'dashboard/server.py:L1965-L1966'
  - symbol: main
    kind: function
    at: 'dashboard/server.py:L1969-L1991'
---
<!-- context:generated:start -->
## Summary

The local web cockpit that monitors and controls the autonomous loop. A ThreadingHTTPServer serves a single-page client (app.js) that polls /api/status and related endpoints, renders state cards, cost panel, hold/release control, directive display, settings, and lazy-loaded auxiliary panels. All directive writes route through the deterministic directive_writer.py to prevent clobbering a PENDING directive, and the settings whitelist prevents writing secrets to runtime.env. Reads only the last 256KB of auto-loop.log per poll to bound work.

## Related

- uses [[autonomous-loop]] — The dashboard's hold/release is the only real loop control; it reads/writes loop state files and the auto-loop.log tail.
- uses [[directive-writer]] — server.py routes all directive writes through directive_writer.py to enforce the PENDING-clobber and body-immutability rules.
- uses [[sentry-reporter]] — server.py reports errors via sentry_client.capture_exception.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
