import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "core"
    / "operator_request_notify.py"
)
SPEC = importlib.util.spec_from_file_location("operator_request_notify", MODULE_PATH)
assert SPEC is not None
assert SPEC.loader is not None
orn = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(orn)


CONSENSUS_SKELETON = """# Consensus

## Active Projects

- `176-R`: SELECTED / ACTIVE VALIDATION.

## WTP Evidence

- NONE.

## Next Action

Do the next thing.
"""


def make_send_fn(results):
    """results: list of (ok, err) tuples returned in call order (last repeats)."""
    calls = []

    def _send(token, chat_id, text):
        calls.append(text)
        idx = min(len(calls) - 1, len(results) - 1)
        return results[idx]

    _send.calls = calls
    return _send


def block_text(req_id, **kw):
    fields = {
        "Status": kw.get("status", "OPEN"),
        "Type": kw.get("type_", "document-procurement"),
        "Blocked scope": kw.get("scope", "208-A"),
        "Required input": kw.get("required", "Complete purchased tender packet."),
        "Acceptable response format": kw.get(
            "fmt", f"human-directive.md entry with Resolves: {req_id}"
        ),
        "Source brief": kw.get("source", "docs/ceo/example.md"),
        "Created": kw.get("created", "2026-07-27T00:00:00Z"),
    }
    lines = [f"## {req_id}", ""]
    for k, v in fields.items():
        lines.append(f"- {k}: {v}")
    for k, v in (kw.get("extra") or {}).items():
        lines.append(f"- {k}: {v}")
    return "\n".join(lines) + "\n\n"


class OperatorRequestNotifyTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.app = Path(self._tmp.name)
        (self.app / "memories").mkdir(parents=True)
        self.requests_path = self.app / "memories" / "operator-requests.md"
        self.consensus_path = self.app / "memories" / "consensus.md"
        self.directive_path = self.app / "memories" / "human-directive.md"
        self.state_path = self.app / "memories" / ".operator-requests-state.json"
        self.consensus_path.write_text(CONSENSUS_SKELETON, encoding="utf-8")
        self.env_patch = mock.patch.dict(
            "os.environ",
            {"TELEGRAM_BOT_TOKEN": "test-token", "TELEGRAM_CHAT_ID": "test-chat"},
        )
        self.env_patch.start()

    def tearDown(self):
        self.env_patch.stop()
        self._tmp.cleanup()

    def write_requests(self, *blocks):
        self.requests_path.write_text(
            orn.TEMPLATE_HEADER + "".join(blocks), encoding="utf-8"
        )

    def noop_sleep(self, _seconds):
        pass

    # 1. A new request is notified exactly once.
    def test_new_request_notified_once(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send = make_send_fn([(True, None)])
        rc = orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertEqual(rc, 0)
        self.assertEqual(len(send.calls), 1)
        self.assertIn("OPREQ-208A-001", send.calls[0])

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertTrue(state["OPREQ-208A-001"]["notified"])

        requests_text = self.requests_path.read_text(encoding="utf-8")
        self.assertIn("Content fingerprint: sha256:", requests_text)

        consensus_text = self.consensus_path.read_text(encoding="utf-8")
        self.assertIn("## Awaiting Operator", consensus_text)
        self.assertIn("OPREQ-208A-001", consensus_text)

    # 2. An unchanged request is not renotified on a second run.
    def test_unchanged_request_not_renotified(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertEqual(len(send.calls), 1)

    # 3a. A timestamp/formatting-only change does NOT trigger a new notification.
    def test_timestamp_only_change_does_not_renotify(self):
        self.write_requests(block_text("OPREQ-208A-001", created="2026-07-27T00:00:00Z"))
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        # Bump only "Created" — material fields (type/scope/required/format/source)
        # are unchanged, so the fingerprint must be identical.
        self.write_requests(block_text("OPREQ-208A-001", created="2026-07-27T09:30:00Z"))
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertEqual(len(send.calls), 1)

    # 3b. A material content change renotifies exactly once.
    def test_material_change_renotifies_once(self):
        self.write_requests(block_text("OPREQ-208A-001", required="Original ask."))
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        self.write_requests(
            block_text("OPREQ-208A-001", required="Materially different ask now.")
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertEqual(len(send.calls), 2)
        self.assertNotEqual(send.calls[0], send.calls[1])

        # And a third identical run must not fire a third notification.
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertEqual(len(send.calls), 2)

    # 4. Ordinary HOLD / informational / research-result types never notify.
    def test_ordinary_hold_type_never_notifies(self):
        self.write_requests(
            block_text("OPREQ-HOLD-001", type_="hold", required="Just a HOLD status."),
            block_text(
                "OPREQ-INFO-001", type_="informational", required="FYI only."
            ),
            block_text(
                "OPREQ-RESEARCH-001",
                type_="research-result",
                required="Some finding.",
            ),
        )
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertEqual(len(send.calls), 0)
        consensus_text = self.consensus_path.read_text(encoding="utf-8")
        self.assertNotIn("OPREQ-HOLD-001", consensus_text)
        self.assertNotIn("OPREQ-INFO-001", consensus_text)
        self.assertNotIn("OPREQ-RESEARCH-001", consensus_text)

    # 5. A Telegram failure must not be recorded as notified; a later success must.
    def test_telegram_failure_not_marked_notified_then_recovers(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        failing = make_send_fn([(False, "network error")])
        orn.main(app_dir=self.app, send_fn=failing, sleep_fn=self.noop_sleep)
        self.assertEqual(len(failing.calls), orn.MAX_ATTEMPTS)

        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertFalse(state["OPREQ-208A-001"]["notified"])
        self.assertIsNotNone(state["OPREQ-208A-001"]["last_error"])
        self.assertEqual(state["OPREQ-208A-001"]["retry_count"], orn.MAX_ATTEMPTS)

        recovering = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=recovering, sleep_fn=self.noop_sleep)
        self.assertEqual(len(recovering.calls), 1)
        state2 = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertTrue(state2["OPREQ-208A-001"]["notified"])

    # 6. A resolved request disappears from the visible projection, and resolution
    #    requires both a directive reference AND recorded evidence — Status: DONE
    #    on the directive alone is not sufficient.
    def test_resolution_requires_evidence_then_disappears_from_projection(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        consensus_text = self.consensus_path.read_text(encoding="utf-8")
        self.assertIn("OPREQ-208A-001", consensus_text)

        # Directive is DONE and references the request, but no Resolution evidence
        # has been recorded yet — must stay OPEN.
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Operator supplied the document set. Resolves: OPREQ-208A-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        requests_text = self.requests_path.read_text(encoding="utf-8")
        blocks = orn.parse_blocks(requests_text)
        self.assertEqual(blocks["OPREQ-208A-001"][0]["Status"], "OPEN")
        consensus_text = self.consensus_path.read_text(encoding="utf-8")
        self.assertIn("OPREQ-208A-001", consensus_text)

        # Now the model records verified resolution evidence in the request block.
        self.write_requests(
            block_text(
                "OPREQ-208A-001",
                extra={
                    "Resolution evidence": (
                        "Operator supplied the full purchased Konak 2026/0003 "
                        "packet; verified all annexes present and paginated."
                    )
                },
            )
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        requests_text = self.requests_path.read_text(encoding="utf-8")
        blocks = orn.parse_blocks(requests_text)
        self.assertEqual(blocks["OPREQ-208A-001"][0]["Status"], "RESOLVED")

        consensus_text = self.consensus_path.read_text(encoding="utf-8")
        self.assertNotIn("OPREQ-208A-001", consensus_text)
        self.assertIn("None currently.", consensus_text)

    # 7. Dedup state round-trips through disk exactly — the property a redeploy's
    #    persistent memories/ volume depends on: a fresh process reading the same
    #    on-disk state must reach the same "already notified" decision.
    def test_dedup_state_persists_across_process_reinstantiation(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send1 = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send1, sleep_fn=self.noop_sleep)
        self.assertEqual(len(send1.calls), 1)

        def _must_not_be_called(token, chat_id, text):
            raise AssertionError("Telegram must not be called for an already-notified, unchanged request")

        send2 = _must_not_be_called
        orn.main(app_dir=self.app, send_fn=send2, sleep_fn=self.noop_sleep)

    # Regression (caught live 2026-07-27 via a self-inflicted root-owned file from
    # manual seeding): a write failure persisting the cosmetic Content-fingerprint
    # rewrite to operator-requests.md must never lose the already-successful
    # Telegram notification's dedup state, and must never crash the script.
    def test_requests_md_write_failure_does_not_lose_notified_state(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send = make_send_fn([(True, None)])
        self.requests_path.chmod(0o444)
        try:
            rc = orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        finally:
            self.requests_path.chmod(0o644)

        self.assertEqual(rc, 0)
        self.assertEqual(len(send.calls), 1)
        state = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertTrue(state["OPREQ-208A-001"]["notified"])

        audit_text = (self.app / "memories" / "operator-requests-audit.log").read_text(
            encoding="utf-8"
        )
        self.assertIn("WRITE-FAILED: operator-requests.md", audit_text)

        # A second, now-writable run must NOT re-send — state survived the failure.
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertEqual(len(send.calls), 1)


if __name__ == "__main__":
    unittest.main()
