---
name: Dashboard server
slug: dashboard-server
type: system
sources:
  - path: dashboard/sentry_client.py
    hash: 96977bb6701f18064edb69c783e53bdb73c930c8ddadcd1caf47583b42700df4
  - path: dashboard/server.py
    hash: 25ddc0141f947f2049909ed903751a78c4e6fcf7718decac740035500f9a972b
sources_digest: 4d0b8c91203ef5299eadc273f387798510d61aed55ef65454aaf5a7266e58dd3
links:
  - to: dashboard-browser-cockpit
    relation: produces
    description: >-
      Serves the /api/status and settings endpoints the browser cockpit polls
      and edits.
  - to: directive-writer-and-promotion-gate
    relation: uses
    description: >-
      write_directive routes through directive_writer.py to enforce locking and
      PENDING protection.
generator:
  version: 1
covers:
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
    at: 'dashboard/server.py:L1122-L1211'
  - symbol: _window_cutoff_epoch
    kind: function
    at: 'dashboard/server.py:L1214-L1242'
  - symbol: read_cost_summary
    kind: function
    at: 'dashboard/server.py:L1245-L1372'
  - symbol: read_tail
    kind: function
    at: 'dashboard/server.py:L1375-L1382'
  - symbol: parse_sections
    kind: function
    at: 'dashboard/server.py:L1385-L1400'
  - symbol: parse_int
    kind: function
    at: 'dashboard/server.py:L1403-L1407'
  - symbol: parse_positive_int
    kind: function
    at: 'dashboard/server.py:L1410-L1415'
  - symbol: parse_key_values
    kind: function
    at: 'dashboard/server.py:L1418-L1425'
  - symbol: blank_parsed
    kind: function
    at: 'dashboard/server.py:L1428-L1452'
  - symbol: parse_windows_status_output
    kind: function
    at: 'dashboard/server.py:L1455-L1537'
  - symbol: parse_macos_status_output
    kind: function
    at: 'dashboard/server.py:L1540-L1576'
  - symbol: read_state_file_pairs
    kind: function
    at: 'dashboard/server.py:L1579-L1587'
  - symbol: run_status_command
    kind: function
    at: 'dashboard/server.py:L1590-L1593'
  - symbol: run_dashboard_action
    kind: function
    at: 'dashboard/server.py:L1596-L1608'
  - symbol: parse_status_output
    kind: function
    at: 'dashboard/server.py:L1611-L1613'
  - symbol: gather_status_payload
    kind: function
    at: 'dashboard/server.py:L1616-L1635'
  - symbol: DashboardHandler
    kind: class
    at: 'dashboard/server.py:L1638-L1943'
  - symbol: _json
    kind: method
    at: 'dashboard/server.py:L1639-L1646'
  - symbol: _text
    kind: method
    at: 'dashboard/server.py:L1648-L1657'
  - symbol: _serve_file
    kind: method
    at: 'dashboard/server.py:L1659-L1663'
  - symbol: do_GET
    kind: method
    at: 'dashboard/server.py:L1665-L1670'
  - symbol: _do_GET
    kind: method
    at: 'dashboard/server.py:L1672-L1738'
  - symbol: _read_body
    kind: method
    at: 'dashboard/server.py:L1740-L1747'
  - symbol: do_POST
    kind: method
    at: 'dashboard/server.py:L1749-L1754'
  - symbol: _do_POST
    kind: method
    at: 'dashboard/server.py:L1756-L1819'
  - symbol: _handle_operator_decision
    kind: method
    at: 'dashboard/server.py:L1821-L1861'
  - symbol: _handle_directive
    kind: method
    at: 'dashboard/server.py:L1863-L1909'
  - symbol: _handle_settings
    kind: method
    at: 'dashboard/server.py:L1911-L1940'
  - symbol: log_message
    kind: method
    at: 'dashboard/server.py:L1942-L1943'
  - symbol: main
    kind: function
    at: 'dashboard/server.py:L1946-L1968'
---
<!-- context:generated:start -->
## Summary

A local HTTP cockpit (ThreadingHTTPServer) for the autonomous loop, serving status, directive editing, operator-request decisions, and runtime settings. Uses a host-profile abstraction to select platform-specific runner/parser functions, routes directive writes through directive_writer.py, parses the operator-request ledger and appends decisions in a layout the verifier expects, and uses tail-window reads on auto-loop.log to bound per-poll work. A whitelist (SETTINGS_SPEC) limits non-secret knobs editable from the panel.

## Related

- produces [[dashboard-browser-cockpit]] — Serves the /api/status and settings endpoints the browser cockpit polls and edits.
- uses [[directive-writer-and-promotion-gate]] — write_directive routes through directive_writer.py to enforce locking and PENDING protection.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
