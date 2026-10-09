---
name: dashboard server
slug: dashboard-server
type: file
sources:
  - path: tests/test_dashboard_server.py
    hash: 56e9073d5a9447df622cb3e0873d553053a3b16089534d427c177db772b933dd
  - path: tests/test_refusal_format.sh
    hash: 11bf5e9869e2e573b4a897e4df84053e4f58d759d3073a9e058705482cc31ef5
sources_digest: 252dbbe5313118bae0e236bc0e3d23e6d95cfee0f02c277a0ab420cd92f01df6
links:
  - to: operator-request-notification-resolution
    relation: produces
    description: The refusal format written by the cockpit panel is consumed downstream
generator:
  version: 1
covers:
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
  - symbol: WeeklyCostWindowTests
    kind: class
    at: 'tests/test_dashboard_server.py:L500-L544'
  - symbol: _summary_for
    kind: method
    at: 'tests/test_dashboard_server.py:L505-L509'
  - symbol: _stamp
    kind: method
    at: 'tests/test_dashboard_server.py:L512-L513'
  - symbol: test_week_window_splits_old_and_new_costs
    kind: method
    at: 'tests/test_dashboard_server.py:L515-L534'
  - symbol: test_unstamped_cost_line_counts_all_time_only
    kind: method
    at: 'tests/test_dashboard_server.py:L536-L544'
  - symbol: LiveBudgetGateDisplayTests
    kind: class
    at: 'tests/test_dashboard_server.py:L547-L581'
  - symbol: test_engine_runtime_parses_live_gate_banner_last_match
    kind: method
    at: 'tests/test_dashboard_server.py:L553-L565'
  - symbol: test_cost_summary_carries_last_budget_gate_line
    kind: method
    at: 'tests/test_dashboard_server.py:L567-L581'
  - symbol: GraftFreshnessTests
    kind: class
    at: 'tests/test_dashboard_server.py:L584-L613'
  - symbol: test_absent_file_reports_unavailable
    kind: method
    at: 'tests/test_dashboard_server.py:L588-L592'
  - symbol: test_valid_status_passthrough
    kind: method
    at: 'tests/test_dashboard_server.py:L594-L604'
  - symbol: test_malformed_json_reports_unavailable
    kind: method
    at: 'tests/test_dashboard_server.py:L606-L613'
---
<!-- context:generated:start -->
## Summary

dashboard/server.py serves status parsing, action dispatch, engine runtime state, settings resolution, cost summary, and log tailing. It parses the persistent auto-loop.log to reflect the latest boot (including escalated cycles and legacy tier lines), anchors spend windows on ccusage blockStart with rolling fallback, splits weekly cost on Monday-UTC, and imports a sibling sentry_client (tests must insert parent dir into sys.path or collection silently fails).

## Related

- produces [[operator-request-notification-resolution]] — The refusal format written by the cockpit panel is consumed downstream
<!-- context:generated:end -->

## Notes

_Anything written below the generated block is preserved when the graph is regenerated._
