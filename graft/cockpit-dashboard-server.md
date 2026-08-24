---
name: Cockpit dashboard server
slug: cockpit-dashboard-server
type: system
sources:
  - path: dashboard/server.py
    hash: 5e7425fc121da8f9caa5984a58b4a28043aec41633ce896f4f371977ccc498ea
sources_digest: d557631a825dfa537342464999f5f5dd0408b904823178b6b638e449dfdd1609
links:
  - to: cockpit-dashboard-ui
    relation: produces
    description: Serves the HTML/JS UI and the REST endpoints the UI consumes.
  - to: directive-writer
    relation: uses
    description: >-
      Routes human-directive.md writes through directive_writer.py for locking,
      atomic rename, and PENDING gate.
  - to: sentry-reporter
    relation: uses
    description: Reports server errors via sentry_client.capture_exception.
generator:
  version: 1
covers:
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
    at: 'dashboard/server.py:L730-L737'
  - symbol: read_settings
    kind: function
    at: 'dashboard/server.py:L740-L782'
  - symbol: write_settings
    kind: function
    at: 'dashboard/server.py:L785-L831'
  - symbol: _proc_cmdline
    kind: function
    at: 'dashboard/server.py:L834-L839'
  - symbol: _proc_ppid
    kind: function
    at: 'dashboard/server.py:L842-L849'
  - symbol: read_hold
    kind: function
    at: 'dashboard/server.py:L856-L879'
  - symbol: set_hold
    kind: function
    at: 'dashboard/server.py:L882-L919'
  - symbol: wake_loop
    kind: function
    at: 'dashboard/server.py:L922-L980'
  - symbol: trigger_redeploy
    kind: function
    at: 'dashboard/server.py:L983-L1019'
  - symbol: _ccusage_compute
    kind: function
    at: 'dashboard/server.py:L1035-L1090'
  - symbol: _run
    kind: function
    at: 'dashboard/server.py:L1041-L1049'
  - symbol: _is_codex
    kind: function
    at: 'dashboard/server.py:L1064-L1066'
  - symbol: read_ccusage
    kind: function
    at: 'dashboard/server.py:L1093-L1113'
  - symbol: _bg
    kind: function
    at: 'dashboard/server.py:L1105-L1110'
  - symbol: read_engine_runtime
    kind: function
    at: 'dashboard/server.py:L1116-L1205'
  - symbol: _window_cutoff_epoch
    kind: function
    at: 'dashboard/server.py:L1208-L1236'
  - symbol: read_cost_summary
    kind: function
    at: 'dashboard/server.py:L1239-L1320'
  - symbol: read_tail
    kind: function
    at: 'dashboard/server.py:L1323-L1330'
  - symbol: parse_sections
    kind: function
    at: 'dashboard/server.py:L1333-L1348'
  - symbol: parse_int
    kind: function
    at: 'dashboard/server.py:L1351-L1355'
  - symbol: parse_positive_int
    kind: function
    at: 'dashboard/server.py:L1358-L1363'
  - symbol: parse_key_values
    kind: function
    at: 'dashboard/server.py:L1366-L1373'
  - symbol: blank_parsed
    kind: function
    at: 'dashboard/server.py:L1376-L1400'
  - symbol: parse_windows_status_output
    kind: function
    at: 'dashboard/server.py:L1403-L1485'
  - symbol: parse_macos_status_output
    kind: function
    at: 'dashboard/server.py:L1488-L1524'
  - symbol: read_state_file_pairs
    kind: function
    at: 'dashboard/server.py:L1527-L1535'
  - symbol: run_status_command
    kind: function
    at: 'dashboard/server.py:L1538-L1541'
  - symbol: run_dashboard_action
    kind: function
    at: 'dashboard/server.py:L1544-L1556'
  - symbol: parse_status_output
    kind: function
    at: 'dashboard/server.py:L1559-L1561'
  - symbol: gather_status_payload
    kind: function
    at: 'dashboard/server.py:L1564-L1583'
  - symbol: DashboardHandler
    kind: class
    at: 'dashboard/server.py:L1586-L1891'
  - symbol: _json
    kind: method
    at: 'dashboard/server.py:L1587-L1594'
  - symbol: _text
    kind: method
    at: 'dashboard/server.py:L1596-L1605'
  - symbol: _serve_file
    kind: method
    at: 'dashboard/server.py:L1607-L1611'
  - symbol: do_GET
    kind: method
    at: 'dashboard/server.py:L1613-L1618'
  - symbol: _do_GET
    kind: method
    at: 'dashboard/server.py:L1620-L1686'
  - symbol: _read_body
    kind: method
    at: 'dashboard/server.py:L1688-L1695'
  - symbol: do_POST
    kind: method
    at: 'dashboard/server.py:L1697-L1702'
  - symbol: _do_POST
    kind: method
    at: 'dashboard/server.py:L1704-L1767'
  - symbol: _handle_operator_decision
    kind: method
    at: 'dashboard/server.py:L1769-L1809'
  - symbol: _handle_directive
    kind: method
    at: 'dashboard/server.py:L1811-L1857'
  - symbol: _handle_settings
    kind: method
    at: 'dashboard/server.py:L1859-L1888'
  - symbol: log_message
    kind: method
    at: 'dashboard/server.py:L1890-L1891'
  - symbol: main
    kind: function
    at: 'dashboard/server.py:L1894-L1916'
---
<!-- context:generated:start -->
## Summary

Local HTTP server for the cockpit UI with platform dispatch (PowerShell vs bash), directive slot read/write via directive_writer, operator-request ledger with load-bearing decision block layout, SETTINGS_SPEC whitelist for runtime.env, tail-read of auto-loop.log, and file-based analyst trigger.

## Related

- produces [[cockpit-dashboard-ui]] — Serves the HTML/JS UI and the REST endpoints the UI consumes.
- uses [[directive-writer]] — Routes human-directive.md writes through directive_writer.py for locking, atomic rename, and PENDING gate.
- uses [[sentry-reporter]] — Reports server errors via sentry_client.capture_exception.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
