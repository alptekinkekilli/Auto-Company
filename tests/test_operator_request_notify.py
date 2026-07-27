import hashlib
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
    #    requires BOTH a directive reference AND a type-specific DETERMINISTIC
    #    verification — the model's own prose can never close its own escalation.
    # 6a. document-procurement: a checksum-matched file on disk under
    #     memories/operator-evidence/<id>/.
    def test_document_procurement_resolution_verifies_checksum_then_disappears(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        consensus_text = self.consensus_path.read_text(encoding="utf-8")
        self.assertIn("OPREQ-208A-001", consensus_text)

        # Directive is DONE and references the request, but no evidence file has
        # been recorded yet — must stay OPEN.
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Operator supplied the document set. Resolves: OPREQ-208A-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-208A-001"][0]["Status"], "OPEN")
        self.assertIn("OPREQ-208A-001", self.consensus_path.read_text(encoding="utf-8"))

        evidence_dir = self.app / "memories" / "operator-evidence" / "OPREQ-208A-001"
        evidence_dir.mkdir(parents=True)
        doc = evidence_dir / "tender-packet.pdf"
        doc.write_bytes(b"fake tender packet bytes for a unit test")
        digest = hashlib.sha256(doc.read_bytes()).hexdigest()

        self.write_requests(
            block_text(
                "OPREQ-208A-001",
                extra={
                    "Evidence files": (
                        "memories/operator-evidence/OPREQ-208A-001/tender-packet.pdf "
                        f"sha256:{digest}"
                    )
                },
            )
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-208A-001"][0]["Status"], "RESOLVED")

        consensus_text = self.consensus_path.read_text(encoding="utf-8")
        self.assertNotIn("OPREQ-208A-001", consensus_text)
        self.assertIn("None currently.", consensus_text)

    # 6b. document-procurement: a tampered/mismatched file must NOT resolve — the
    #     model cannot just claim a checksum, the code recomputes and compares it.
    def test_document_procurement_resolution_blocks_on_checksum_mismatch(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        evidence_dir = self.app / "memories" / "operator-evidence" / "OPREQ-208A-001"
        evidence_dir.mkdir(parents=True)
        (evidence_dir / "tender-packet.pdf").write_bytes(b"real content")

        self.write_requests(
            block_text(
                "OPREQ-208A-001",
                extra={
                    "Evidence files": (
                        "memories/operator-evidence/OPREQ-208A-001/tender-packet.pdf "
                        "sha256:" + "0" * 64
                    )
                },
            )
        )
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-208A-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-208A-001"][0]["Status"], "OPEN")
        audit_text = (
            self.app / "memories" / "operator-requests-audit.log"
        ).read_text(encoding="utf-8")
        self.assertIn("checksum mismatch", audit_text)

    # 6c. document-procurement: a path outside memories/operator-evidence/ must be
    #     refused, not silently checksummed wherever it happens to live.
    def test_document_procurement_resolution_blocks_path_outside_evidence_dir(self):
        self.write_requests(block_text("OPREQ-208A-001"))
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        outside = self.app / "memories" / "consensus.md"
        digest = hashlib.sha256(outside.read_bytes()).hexdigest()

        self.write_requests(
            block_text(
                "OPREQ-208A-001",
                extra={"Evidence files": f"memories/consensus.md sha256:{digest}"},
            )
        )
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-208A-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-208A-001"][0]["Status"], "OPEN")
        audit_text = (
            self.app / "memories" / "operator-requests-audit.log"
        ).read_text(encoding="utf-8")
        self.assertIn("outside memories/operator-evidence/", audit_text)

    # 6d. credential: requires a non-mutating PASS test log with no secret-shaped
    #     content — the credential value itself is never written anywhere.
    def test_credential_resolution_requires_pass_log_without_secrets(self):
        self.write_requests(
            block_text(
                "OPREQ-CRED-001",
                type_="credential",
                required="EKAP bidder-account login for firm X.",
                scope="external-firm-x",
            )
        )
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        evidence_dir = self.app / "memories" / "operator-evidence" / "OPREQ-CRED-001"
        evidence_dir.mkdir(parents=True)
        (evidence_dir / "auth-test.log").write_text(
            "Logged in, viewed profile page, performed no mutation.", encoding="utf-8"
        )

        self.write_requests(
            block_text(
                "OPREQ-CRED-001",
                type_="credential",
                required="EKAP bidder-account login for firm X.",
                scope="external-firm-x",
                extra={
                    "Verification method": "EKAP login, read-only profile view",
                    "Verification result": "PASS",
                    "Verification timestamp": "2026-07-27T15:00:00Z",
                    "Verification log": (
                        "memories/operator-evidence/OPREQ-CRED-001/auth-test.log"
                    ),
                },
            )
        )
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-CRED-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-CRED-001"][0]["Status"], "RESOLVED")

    def test_credential_resolution_blocks_if_log_contains_secret_shaped_token(self):
        self.write_requests(
            block_text(
                "OPREQ-CRED-001",
                type_="credential",
                required="EKAP bidder-account login for firm X.",
                scope="external-firm-x",
            )
        )
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        evidence_dir = self.app / "memories" / "operator-evidence" / "OPREQ-CRED-001"
        evidence_dir.mkdir(parents=True)
        (evidence_dir / "auth-test.log").write_text(
            "Bearer abcdefghijklmnopqrstuvwxyz01234567", encoding="utf-8"
        )

        self.write_requests(
            block_text(
                "OPREQ-CRED-001",
                type_="credential",
                required="EKAP bidder-account login for firm X.",
                scope="external-firm-x",
                extra={
                    "Verification method": "EKAP login, read-only profile view",
                    "Verification result": "PASS",
                    "Verification timestamp": "2026-07-27T15:00:00Z",
                    "Verification log": (
                        "memories/operator-evidence/OPREQ-CRED-001/auth-test.log"
                    ),
                },
            )
        )
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-CRED-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-CRED-001"][0]["Status"], "OPEN")
        audit_text = (
            self.app / "memories" / "operator-requests-audit.log"
        ).read_text(encoding="utf-8")
        self.assertIn("secret-shaped", audit_text)

    # 6e. legal-decision / financial-decision: require a structured
    #     "Decision for OPREQ-<id>: <word> — <rationale>" line the OPERATOR wrote
    #     into human-directive.md — the model's own evidence field is never enough.
    def test_legal_decision_resolution_requires_structured_decision_line(self):
        self.write_requests(
            block_text(
                "OPREQ-LEGAL-001",
                type_="legal-decision",
                required="Approve or deny the pivot.",
                scope="GLOBAL",
            )
        )
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        # References it and is DONE, but has no structured Decision line.
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "I approve this. Resolves: OPREQ-LEGAL-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-LEGAL-001"][0]["Status"], "OPEN")

        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-LEGAL-001\n"
            "Decision for OPREQ-LEGAL-001: APPROVED — cleared by counsel review.\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-LEGAL-001"][0]["Status"], "RESOLVED")

    # 6g. adjudication-pending: reuses the legal/financial structured-decision
    #     verifier — applying an external adjudicator's ruling requires the
    #     same "Decision for OPREQ-<id>: ..." line the OPERATOR wrote, not a
    #     model claim that the ruling arrived.
    def test_adjudication_pending_resolution_requires_structured_decision_line(self):
        self.write_requests(
            block_text(
                "OPREQ-ADJ-001",
                type_="adjudication-pending",
                required=(
                    "Take the evidence pack to an independent high-capability "
                    "model and apply its ruling."
                ),
                scope="GLOBAL",
            )
        )
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        self.assertIn(
            "OPREQ-ADJ-001", self.consensus_path.read_text(encoding="utf-8")
        )

        # References it and is DONE, but no structured Decision line yet.
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Applied the ruling. Resolves: OPREQ-ADJ-001\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-ADJ-001"][0]["Status"], "OPEN")

        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-ADJ-001\n"
            "Decision for OPREQ-ADJ-001: PIVOT — external ruling applied verbatim.\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-ADJ-001"][0]["Status"], "RESOLVED")
        self.assertNotIn(
            "OPREQ-ADJ-001", self.consensus_path.read_text(encoding="utf-8")
        )

    # 6f. expenditure-approval / external-action-authorization: require a
    #     structured "Authorization for OPREQ-<id>:" block (System/Action/Target/
    #     Limit) the OPERATOR wrote into human-directive.md.
    def test_expenditure_resolution_requires_structured_authorization_block(self):
        self.write_requests(
            block_text(
                "OPREQ-SPEND-001",
                type_="expenditure-approval",
                required="Approve TRY 2,000 tender-document purchase.",
                scope="208-A",
            )
        )
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)

        # Incomplete block (missing Limit) must stay OPEN.
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-SPEND-001\n"
            "Authorization for OPREQ-SPEND-001:\n"
            "System: Konak tender authority portal\n"
            "Action: purchase document set\n"
            "Target: Konak 2026/0003\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-SPEND-001"][0]["Status"], "OPEN")

        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n"
            "Resolves: OPREQ-SPEND-001\n"
            "Authorization for OPREQ-SPEND-001:\n"
            "System: Konak tender authority portal\n"
            "Action: purchase document set\n"
            "Target: Konak 2026/0003\n"
            "Limit: TRY 2,000\n",
            encoding="utf-8",
        )
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        blocks = orn.parse_blocks(self.requests_path.read_text(encoding="utf-8"))
        self.assertEqual(blocks["OPREQ-SPEND-001"][0]["Status"], "RESOLVED")

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
