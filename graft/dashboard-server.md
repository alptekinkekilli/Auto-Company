---
name: Dashboard server
slug: dashboard-server
type: system
sources:
  - path: dashboard/server.py
    hash: 3a229baecad68a23203f56f1e8fd55d005b2e803027f893e06c708ad40835c64
  - path: tests/test_dashboard_server.py
    hash: 5af6c4f462552608f0f6d47fcab10935ceba1edfa0741d94c5081ba35a3b7e66
sources_digest: ba4cf20d6f6f5b07cf3410b4e80cb0c2eae42c1b491479f78390c448ccc55e88
links:
  - to: auto-loop-core-engine
    relation: uses
    description: Reads auto-loop.log and router-state content produced by the loop.
  - to: escalation-and-operator-requests
    relation: produces
    description: >-
      The operator-decision panel writes the refusal format consumed by
      operator_request_notify.py.
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
  - symbol: _ccusage_compute
    kind: function
    at: 'dashboard/server.py:L1031-L1086'
  - symbol: _run
    kind: function
    at: 'dashboard/server.py:L1037-L1045'
  - symbol: _is_codex
    kind: function
    at: 'dashboard/server.py:L1060-L1062'
  - symbol: read_ccusage
    kind: function
    at: 'dashboard/server.py:L1089-L1109'
  - symbol: _bg
    kind: function
    at: 'dashboard/server.py:L1101-L1106'
  - symbol: read_engine_runtime
    kind: function
    at: 'dashboard/server.py:L1112-L1201'
  - symbol: _window_cutoff_epoch
    kind: function
    at: 'dashboard/server.py:L1204-L1232'
  - symbol: read_cost_summary
    kind: function
    at: 'dashboard/server.py:L1235-L1316'
  - symbol: read_tail
    kind: function
    at: 'dashboard/server.py:L1319-L1326'
  - symbol: parse_sections
    kind: function
    at: 'dashboard/server.py:L1329-L1344'
  - symbol: parse_int
    kind: function
    at: 'dashboard/server.py:L1347-L1351'
  - symbol: parse_positive_int
    kind: function
    at: 'dashboard/server.py:L1354-L1359'
  - symbol: parse_key_values
    kind: function
    at: 'dashboard/server.py:L1362-L1369'
  - symbol: blank_parsed
    kind: function
    at: 'dashboard/server.py:L1372-L1396'
  - symbol: parse_windows_status_output
    kind: function
    at: 'dashboard/server.py:L1399-L1481'
  - symbol: parse_macos_status_output
    kind: function
    at: 'dashboard/server.py:L1484-L1520'
  - symbol: read_state_file_pairs
    kind: function
    at: 'dashboard/server.py:L1523-L1531'
  - symbol: run_status_command
    kind: function
    at: 'dashboard/server.py:L1534-L1537'
  - symbol: run_dashboard_action
    kind: function
    at: 'dashboard/server.py:L1540-L1552'
  - symbol: parse_status_output
    kind: function
    at: 'dashboard/server.py:L1555-L1557'
  - symbol: gather_status_payload
    kind: function
    at: 'dashboard/server.py:L1560-L1579'
  - symbol: DashboardHandler
    kind: class
    at: 'dashboard/server.py:L1582-L1887'
  - symbol: _json
    kind: method
    at: 'dashboard/server.py:L1583-L1590'
  - symbol: _text
    kind: method
    at: 'dashboard/server.py:L1592-L1601'
  - symbol: _serve_file
    kind: method
    at: 'dashboard/server.py:L1603-L1607'
  - symbol: do_GET
    kind: method
    at: 'dashboard/server.py:L1609-L1614'
  - symbol: _do_GET
    kind: method
    at: 'dashboard/server.py:L1616-L1682'
  - symbol: _read_body
    kind: method
    at: 'dashboard/server.py:L1684-L1691'
  - symbol: do_POST
    kind: method
    at: 'dashboard/server.py:L1693-L1698'
  - symbol: _do_POST
    kind: method
    at: 'dashboard/server.py:L1700-L1763'
  - symbol: _handle_operator_decision
    kind: method
    at: 'dashboard/server.py:L1765-L1805'
  - symbol: _handle_directive
    kind: method
    at: 'dashboard/server.py:L1807-L1853'
  - symbol: _handle_settings
    kind: method
    at: 'dashboard/server.py:L1855-L1884'
  - symbol: log_message
    kind: method
    at: 'dashboard/server.py:L1886-L1887'
  - symbol: main
    kind: function
    at: 'dashboard/server.py:L1890-L1912'
  - symbol: DashboardServerTests
    kind: class
    at: 'tests/test_dashboard_server.py:L27-L210'
  - symbol: test_windows_not_running_maps_to_stopped
    kind: method
    at: 'tests/test_dashboard_server.py:L28-L52'
  - symbol: test_windows_not_installed_daemon_maps_correctly
    kind: method
    at: 'tests/test_dashboard_server.py:L54-L74'
  - symbol: test_macos_active_configured_running_maps_correctly
    kind: method
    at: 'tests/test_dashboard_server.py:L76-L112'
  - symbol: test_macos_inactive_configured_stopped_and_guardian_without_caffeinate
    kind: method
    at: 'tests/test_dashboard_server.py:L114-L135'
  - symbol: test_macos_not_installed_maps_correctly
    kind: method
    at: 'tests/test_dashboard_server.py:L137-L157'
  - symbol: test_windows_start_uses_powershell_runner
    kind: method
    at: 'tests/test_dashboard_server.py:L159-L169'
  - symbol: test_macos_stop_uses_shell_runner_with_pause_daemon
    kind: method
    at: 'tests/test_dashboard_server.py:L171-L183'
  - symbol: test_refresh_uses_status_script
    kind: method
    at: 'tests/test_dashboard_server.py:L185-L194'
  - symbol: test_invalid_log_tail_lines_fall_back_to_default
    kind: method
    at: 'tests/test_dashboard_server.py:L196-L199'
  - symbol: test_unsupported_host_raises
    kind: method
    at: 'tests/test_dashboard_server.py:L201-L210'
  - symbol: EngineRuntimeParsingTests
    kind: class
    at: 'tests/test_dashboard_server.py:L235-L368'
  - symbol: _run
    kind: method
    at: 'tests/test_dashboard_server.py:L238-L243'
  - symbol: fake_read
    kind: function
    at: 'tests/test_dashboard_server.py:L239-L240'
  - symbol: test_claude_cycle_reports_its_effort
    kind: method
    at: 'tests/test_dashboard_server.py:L245-L253'
  - symbol: test_codex_cycle_still_reports_codex_effort
    kind: method
    at: 'tests/test_dashboard_server.py:L255-L259'
  - symbol: test_window_budget_and_ladders_take_the_latest_boot
    kind: method
    at: 'tests/test_dashboard_server.py:L261-L271'
  - symbol: test_legacy_tier_line_without_claude_effort_still_parses
    kind: method
    at: 'tests/test_dashboard_server.py:L273-L284'
  - symbol: _settings
    kind: method
    at: 'tests/test_dashboard_server.py:L292-L296'
  - symbol: test_settings_source_runtime_env_wins
    kind: method
    at: 'tests/test_dashboard_server.py:L298-L303'
  - symbol: test_settings_source_container_when_absent_from_file
    kind: method
    at: 'tests/test_dashboard_server.py:L305-L310'
  - symbol: test_settings_source_default_when_nowhere
    kind: method
    at: 'tests/test_dashboard_server.py:L312-L315'
  - symbol: _runtime
    kind: method
    at: 'tests/test_dashboard_server.py:L332-L340'
  - symbol: fake_read
    kind: function
    at: 'tests/test_dashboard_server.py:L333-L334'
  - symbol: test_escalated_cycle_reports_the_escalated_model
    kind: method
    at: 'tests/test_dashboard_server.py:L342-L348'
  - symbol: test_escalation_before_the_tier_line_is_ignored
    kind: method
    at: 'tests/test_dashboard_server.py:L350-L363'
  - symbol: test_codex_cycle_ignores_escalation_entirely
    kind: method
    at: 'tests/test_dashboard_server.py:L365-L368'
  - symbol: WindowCutoffTests
    kind: class
    at: 'tests/test_dashboard_server.py:L371-L432'
  - symbol: setUp
    kind: method
    at: 'tests/test_dashboard_server.py:L379-L386'
  - symbol: tearDown
    kind: method
    at: 'tests/test_dashboard_server.py:L388-L390'
  - symbol: _write
    kind: method
    at: 'tests/test_dashboard_server.py:L392-L396'
  - symbol: test_fresh_blockstart_anchors_the_window
    kind: method
    at: 'tests/test_dashboard_server.py:L398-L404'
  - symbol: test_stale_usage_file_falls_back_to_rolling
    kind: method
    at: 'tests/test_dashboard_server.py:L406-L414'
  - symbol: test_blockstart_older_than_rolling_never_widens_the_window
    kind: method
    at: 'tests/test_dashboard_server.py:L416-L421'
  - symbol: test_missing_or_unparseable_file_falls_back
    kind: method
    at: 'tests/test_dashboard_server.py:L423-L432'
  - symbol: ReadTextFileTailTests
    kind: class
    at: 'tests/test_dashboard_server.py:L439-L497'
  - symbol: _tmp
    kind: method
    at: 'tests/test_dashboard_server.py:L444-L449'
  - symbol: test_returns_whole_file_when_smaller_than_window
    kind: method
    at: 'tests/test_dashboard_server.py:L451-L455'
  - symbol: test_truncates_to_the_tail_and_drops_the_partial_first_line
    kind: method
    at: 'tests/test_dashboard_server.py:L457-L464'
  - symbol: test_multibyte_seek_does_not_produce_replacement_junk
    kind: method
    at: 'tests/test_dashboard_server.py:L466-L470'
  - symbol: test_missing_file_returns_fallback
    kind: method
    at: 'tests/test_dashboard_server.py:L472-L475'
  - symbol: test_engine_runtime_falls_back_to_full_file_when_banner_is_out_of_window
    kind: method
    at: 'tests/test_dashboard_server.py:L477-L497'
  - symbol: fake_read
    kind: function
    at: 'tests/test_dashboard_server.py:L488-L489'
---
<!-- context:generated:start -->
## Summary

dashboard/server.py parses status output, reads engine runtime and settings from auto-loop.log, and dispatches operator-decision actions. The spend window matches the loop's blockStart-anchored enforcement rather than a rolling fallback; read_text_file_tail truncates safely without mid-line or multibyte corruption.

## Related

- uses [[auto-loop-core-engine]] — Reads auto-loop.log and router-state content produced by the loop.
- produces [[escalation-and-operator-requests]] — The operator-decision panel writes the refusal format consumed by operator_request_notify.py.
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
