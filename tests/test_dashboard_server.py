import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


SERVER_PATH = Path(__file__).resolve().parents[1] / "dashboard" / "server.py"
# server.py imports its sibling `sentry_client`. Loading it by file path does NOT
# put dashboard/ on sys.path (production gets that for free from `python
# dashboard/server.py`), so without this the whole module fails to import and all
# of these tests are skipped as a single collection error — silently, since a
# missing module reads like an environment problem rather than a dead suite.
sys.path.insert(0, str(SERVER_PATH.parent))
SPEC = importlib.util.spec_from_file_location("dashboard_server", SERVER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
dashboard_server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard_server)


class DashboardServerTests(unittest.TestCase):
    def test_windows_not_running_maps_to_stopped(self) -> None:
        raw = """=== Windows Guardian ===
Awake guardian: STOPPED

=== Windows Autostart Task ===
Autostart: NOT CONFIGURED

=== WSL Daemon (systemd --user) ===
active
MainPID=321
ActiveState=active
SubState=running

=== Auto Company Status ===
Loop: NOT RUNNING
Daemon: ACTIVE (systemd --user auto-company.service)
ENGINE=claude
MODEL=sonnet
"""
        parsed = dashboard_server.parse_status_output(raw, system_name="Windows")
        self.assertEqual(parsed["guardian"]["state"], "stopped")
        self.assertEqual(parsed["autostart"]["state"], "not_configured")
        self.assertEqual(parsed["daemon"]["state"], "active")
        self.assertEqual(parsed["loop"]["state"], "stopped")
        self.assertIsNone(parsed["loop"]["pid"])

    def test_windows_not_installed_daemon_maps_correctly(self) -> None:
        raw = """=== Windows Guardian ===
Awake guardian: RUNNING (PID 45)

=== Windows Autostart Task ===
Autostart: CONFIGURED (AutoCompany-WSL-Start)

=== WSL Daemon (systemd --user) ===
auto-company.service: not installed

=== Auto Company Status ===
Loop: RUNNING (PID 77)
Daemon: NOT INSTALLED (systemd --user auto-company.service)
"""
        parsed = dashboard_server.parse_status_output(raw, system_name="Windows")
        self.assertEqual(parsed["guardian"]["state"], "running")
        self.assertEqual(parsed["guardian"]["pid"], 45)
        self.assertEqual(parsed["autostart"]["state"], "configured")
        self.assertEqual(parsed["daemon"]["state"], "not_installed")
        self.assertEqual(parsed["loop"]["state"], "running")
        self.assertEqual(parsed["loop"]["pid"], 77)

    def test_macos_active_configured_running_maps_correctly(self) -> None:
        raw = """=== Guardian ===
State=running
Pid=111
Raw=caffeinate -w 456

=== Daemon ===
State=active
MainPID=222
Raw=launchd agent loaded

=== Autostart ===
State=configured
Raw=LaunchAgent plist present

=== Loop ===
State=running
Pid=456
Raw=Loop running

=== State File ===
ENGINE=claude
MODEL=sonnet
LOOP_COUNT=9
ERROR_COUNT=0
LAST_RUN=2026-03-14 12:00:00
"""
        parsed = dashboard_server.parse_status_output(raw, system_name="Darwin")
        self.assertEqual(parsed["guardian"]["state"], "running")
        self.assertEqual(parsed["guardian"]["pid"], 111)
        self.assertEqual(parsed["daemon"]["state"], "active")
        self.assertEqual(parsed["daemon"]["mainPid"], 222)
        self.assertEqual(parsed["autostart"]["state"], "configured")
        self.assertEqual(parsed["loop"]["state"], "running")
        self.assertEqual(parsed["loop"]["pid"], 456)
        self.assertEqual(parsed["loop"]["engine"], "claude")
        self.assertEqual(parsed["loop"]["loopCount"], "9")

    def test_macos_inactive_configured_stopped_and_guardian_without_caffeinate(self) -> None:
        raw = """=== Guardian ===
State=stopped
Raw=Sleep guard: loop running without caffeinate

=== Daemon ===
State=inactive
Raw=LaunchAgent paused (.auto-loop-paused present)

=== Autostart ===
State=configured
Raw=LaunchAgent plist present

=== Loop ===
State=stopped
Raw=Loop stopped (stale PID 456)
"""
        parsed = dashboard_server.parse_status_output(raw, system_name="Darwin")
        self.assertEqual(parsed["guardian"]["state"], "stopped")
        self.assertEqual(parsed["daemon"]["state"], "inactive")
        self.assertEqual(parsed["autostart"]["state"], "configured")
        self.assertEqual(parsed["loop"]["state"], "stopped")

    def test_macos_not_installed_maps_correctly(self) -> None:
        raw = """=== Guardian ===
State=stopped
Raw=Sleep guard: not active

=== Daemon ===
State=not_installed
Raw=LaunchAgent plist not installed

=== Autostart ===
State=not_configured
Raw=LaunchAgent plist absent

=== Loop ===
State=stopped
Raw=Loop not running
"""
        parsed = dashboard_server.parse_status_output(raw, system_name="Darwin")
        self.assertEqual(parsed["daemon"]["state"], "not_installed")
        self.assertEqual(parsed["autostart"]["state"], "not_configured")
        self.assertEqual(parsed["loop"]["state"], "stopped")

    def test_windows_start_uses_powershell_runner(self) -> None:
        with mock.patch.object(
            dashboard_server,
            "run_powershell_script",
            return_value={"ok": True, "exitCode": 0, "elapsedMs": 1, "output": ""},
        ) as runner:
            result = dashboard_server.run_dashboard_action("start", system_name="Windows")
        self.assertTrue(result["ok"])
        runner.assert_called_once_with(
            dashboard_server.WINDOWS_START_SCRIPT, args=None, timeout=120
        )

    def test_macos_stop_uses_shell_runner_with_pause_daemon(self) -> None:
        with mock.patch.object(
            dashboard_server,
            "run_shell_script",
            return_value={"ok": True, "exitCode": 0, "elapsedMs": 1, "output": ""},
        ) as runner:
            result = dashboard_server.run_dashboard_action("stop", system_name="Darwin")
        self.assertTrue(result["ok"])
        runner.assert_called_once_with(
            dashboard_server.MACOS_STOP_SCRIPT,
            args=["--pause-daemon"],
            timeout=120,
        )

    def test_refresh_uses_status_script(self) -> None:
        with mock.patch.object(
            dashboard_server,
            "run_shell_script",
            return_value={"ok": True, "exitCode": 0, "elapsedMs": 1, "output": ""},
        ) as runner:
            dashboard_server.run_dashboard_action("refresh", system_name="Darwin")
        runner.assert_called_once_with(
            dashboard_server.MACOS_STATUS_SCRIPT, timeout=90
        )

    def test_invalid_log_tail_lines_fall_back_to_default(self) -> None:
        self.assertEqual(dashboard_server.parse_positive_int("abc", default=180), 180)
        self.assertEqual(dashboard_server.parse_positive_int("-5", default=180), 180)
        self.assertEqual(dashboard_server.parse_positive_int("12", default=180), 12)

    def test_unsupported_host_raises(self) -> None:
        # Was asserting that "Linux" raises. Linux/container support was added to
        # detect_host_kind() (the company itself runs in a Linux container) but
        # this test was never updated, so it had been failing independently of
        # the change it now sits beside. Assert the real contract instead:
        # Windows/Darwin/Linux resolve, anything else raises.
        self.assertEqual(dashboard_server.detect_host_kind("Linux"),
                         dashboard_server.LINUX_HOST)
        with self.assertRaisesRegex(RuntimeError, "only supports Windows"):
            dashboard_server.detect_host_kind("Plan9")


# auto-loop.log is persistent across redeploys, so the Runtime State panel is
# parsing a file that contains every historical boot. These cover the 2026-07-28
# regressions where three fields were pinned to a 2026-07-21 boot line.
STALE_THEN_CURRENT_LOG = """\
[2026-07-21 19:02:10] Interval: 60s | Timeout: 1800s | Breaker: 5 errors
[2026-07-21 19:02:10] Window budget: $8 per 18000s (pause 1800s when reached)
[2026-07-21 19:02:10] Tier ladder: ON (round-robin) | \
Claude [claude-haiku-4-5-20251001,claude-sonnet-5] | Codex effort [low,medium]
[2026-07-21 19:02:11] [ROUTER] Alternate -> Claude (old)
[2026-07-21 19:02:11] [TIER] round-robin -> Claude=claude-haiku-4-5-20251001 \
[claude $0.10/8], Codex effort=medium [codex 0/5]
[2026-07-28 08:59:17] Interval: 900s | Timeout: 1800s | Breaker: 5 errors
[2026-07-28 08:59:17] Window budget: $40 per 18000s (pause 1800s when reached)
[2026-07-28 08:59:17] Tier ladder: ON (round-robin) | \
Claude [claude-sonnet-5:low,claude-sonnet-5:high,claude-opus-5:high] | \
Codex effort [low,medium,high]
[2026-07-28 08:59:17] [ROUTER] Alternate -> Claude (both have headroom)
[2026-07-28 08:59:17] [TIER] fill-weighted -> Claude=claude-opus-5 effort=high \
[claude $3.1630/40.00], Codex effort=low [codex 1/inf]
"""


class EngineRuntimeParsingTests(unittest.TestCase):
    """read_engine_runtime() must reflect the LATEST boot, not the first one."""

    def _run(self, log_text: str, router_state: str) -> dict:
        def fake_read(path, default=""):
            return router_state if path.name == "router-state" else log_text

        with mock.patch.object(dashboard_server, "read_text_file", fake_read):
            return dashboard_server.read_engine_runtime()

    def test_claude_cycle_reports_its_effort(self) -> None:
        # Regression: routedEffort was hardcoded "" on the Claude branch, so the
        # panel could never show which rung ran — and the live ladder's rungs
        # differ only by effort.
        out = self._run(STALE_THEN_CURRENT_LOG, "claude")
        self.assertEqual(out["routedEngine"], "claude")
        self.assertEqual(out["routedModel"], "claude-opus-5")
        self.assertEqual(out["routedEffort"], "high")
        self.assertEqual(out["claudeEffort"], "high")

    def test_codex_cycle_still_reports_codex_effort(self) -> None:
        out = self._run(STALE_THEN_CURRENT_LOG, "codex")
        self.assertEqual(out["routedEffort"], "low")
        # The Claude-ladder pick is still surfaced separately on a Codex cycle.
        self.assertEqual(out["claudePick"], "claude-opus-5")

    def test_window_budget_and_ladders_take_the_latest_boot(self) -> None:
        # Regression: re.search() returned the FIRST match, so the panel showed
        # a $8 cap and a haiku/sonnet ladder days after both had changed.
        out = self._run(STALE_THEN_CURRENT_LOG, "claude")
        self.assertEqual(out["windowBudget"], "40")
        self.assertEqual(out["interval"], "900")
        self.assertEqual(
            out["claudeLadder"],
            ["claude-sonnet-5:low", "claude-sonnet-5:high", "claude-opus-5:high"],
        )
        self.assertEqual(out["codexLadder"], ["low", "medium", "high"])

    def test_legacy_tier_line_without_claude_effort_still_parses(self) -> None:
        # Pre-APP-241 lines carry no `effort=` after the model. Requiring it
        # would silently fall back to an even older line.
        legacy_only = (
            "[2026-07-21 19:02:10] Window budget: $8 per 18000s (pause 1800s when reached)\n"
            "[2026-07-21 19:02:11] [TIER] round-robin -> Claude=claude-sonnet-5 "
            "[claude $0.10/8], Codex effort=medium [codex 0/5]\n"
        )
        out = self._run(legacy_only, "claude")
        self.assertEqual(out["routedModel"], "claude-sonnet-5")
        self.assertEqual(out["routedEffort"], "")
        self.assertEqual(out["codexEffort"], "medium")


if __name__ == "__main__":
    unittest.main()


class ReadTextFileTailTests(unittest.TestCase):
    """auto-loop.log is persistent and ever-growing; the status poll must not
    re-parse all of it. Correctness rule: everything read from it takes the LAST
    match, so a tail is fine — but the once-per-boot banner must still be found."""

    def _tmp(self, content: bytes):
        import tempfile
        d = tempfile.mkdtemp()
        p = Path(d) / "auto-loop.log"
        p.write_bytes(content)
        return p

    def test_returns_whole_file_when_smaller_than_window(self) -> None:
        p = self._tmp(b"line one\nline two\n")
        self.assertEqual(
            dashboard_server.read_text_file_tail(p, 1_000_000), "line one\nline two\n"
        )

    def test_truncates_to_the_tail_and_drops_the_partial_first_line(self) -> None:
        body = ("".join(f"line {i}\n" for i in range(1000))).encode()
        p = self._tmp(body)
        out = dashboard_server.read_text_file_tail(p, 200)
        self.assertLessEqual(len(out.encode()), 200)
        self.assertTrue(out.endswith("line 999\n"))
        # never starts mid-line
        self.assertTrue(out.startswith("line "))

    def test_multibyte_seek_does_not_produce_replacement_junk(self) -> None:
        body = ("".join(f"satır-{i} ölçüm\n" for i in range(500))).encode("utf-8")
        p = self._tmp(body)
        out = dashboard_server.read_text_file_tail(p, 201)
        self.assertNotIn("�", out)

    def test_missing_file_returns_fallback(self) -> None:
        self.assertEqual(
            dashboard_server.read_text_file_tail(Path("/nope/none.log"), 100, "fb"), "fb"
        )

    def test_engine_runtime_falls_back_to_full_file_when_banner_is_out_of_window(self) -> None:
        # Banner at the very top, then more than the window's worth of churn after it.
        banner = (
            "Tier ladder: ON (round-robin) | Claude [claude-sonnet-5:low] | "
            "Codex effort [low,medium]\n"
            "Window budget: $40 per 18000s (pause 1800s when reached)\n"
        )
        churn = "".join(f"[TIER] fill-weighted -> Claude=m{i} effort=low [claude $1/40], "
                        f"Codex effort=low [codex 1/2]\n" for i in range(3000))
        p = self._tmp((banner + churn).encode())

        def fake_read(path, default=""):
            return "claude" if path.name == "router-state" else p.read_text()

        with mock.patch.object(dashboard_server, "LOG_FILE", p), \
             mock.patch.object(dashboard_server, "ENGINE_RUNTIME_TAIL_BYTES", 2000), \
             mock.patch.object(dashboard_server, "read_text_file", fake_read):
            out = dashboard_server.read_engine_runtime()
        # Recovered from the full file rather than silently losing the fields.
        self.assertEqual(out["windowBudget"], "40")
        self.assertEqual(out["claudeLadder"], ["claude-sonnet-5:low"])
