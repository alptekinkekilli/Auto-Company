import hashlib
import importlib.util
import json
import re
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

    # --- verify_authorization: an empty field must never borrow the next line ---
    #
    # The ledger promises the operator that "any missing or empty line leaves this
    # request OPEN". Before the `[^\n]+` fix it did the opposite: `\s` matches a
    # newline, so a bare `System:` captured the `Action:` line as its value and the
    # block passed. That closes an authorization with a value nobody wrote — a
    # silent-wrong-close, strictly worse than a silent-stay-open.

    AUTH_BLOCK = (
        "Resolves: OPREQ-TEST-AUTH-001\n\n"
        "Authorization for OPREQ-TEST-AUTH-001:\n"
        "System: OpenTimestamps public calendar servers\n"
        "Action: submit a SHA-256 digest and store the receipt\n"
        "Target: opentimestamps.org only\n"
        "Limit: at most 30 submissions, expires in 14 days\n\n"
        "Record each submission in the fixture work ledger.\n"
    )

    def test_authorization_complete_block_passes(self):
        ok, msg = orn.verify_authorization("OPREQ-TEST-AUTH-001", self.AUTH_BLOCK)
        self.assertTrue(ok, msg)
        self.assertIn("OpenTimestamps", msg)

    def test_authorization_blank_field_does_not_borrow_next_line(self):
        for label in ("System", "Action", "Target", "Limit"):
            with self.subTest(label=label):
                blanked = re.sub(
                    rf"^{label}:.*$", f"{label}:", self.AUTH_BLOCK, count=1, flags=re.M
                )
                ok, msg = orn.verify_authorization("OPREQ-TEST-AUTH-001", blanked)
                self.assertFalse(ok, f"blank {label} wrongly accepted: {msg}")
                self.assertIn(label, msg)

    def test_authorization_missing_field_reported(self):
        dropped = re.sub(r"^Target:.*\n", "", self.AUTH_BLOCK, count=1, flags=re.M)
        ok, msg = orn.verify_authorization("OPREQ-TEST-AUTH-001", dropped)
        self.assertFalse(ok)
        self.assertIn("Target", msg)

    # --- REFUSE: a refusal is a decision, and it must actually close the request ---
    #
    # The ledger promised "an entry containing Resolves: <id> and the word REFUSE"
    # since the mechanism shipped, and nothing implemented it: the refusal fell
    # through to the type verifier, failed for want of an authorization block, and
    # left the request OPEN with only an audit line nobody watches.

    def _refuse_run(self, directive: str, *blocks):
        self.write_requests(*blocks)
        self.directive_path.write_text(
            "# Human Directive\n\n## Status\nDONE\n\n## Directive\n" + directive,
            encoding="utf-8",
        )
        send = make_send_fn([(True, None)])
        orn.main(app_dir=self.app, send_fn=send, sleep_fn=self.noop_sleep)
        return self.requests_path.read_text(encoding="utf-8")

    def test_refuse_closes_the_request_as_refused_not_resolved(self):
        out = self._refuse_run(
            "Resolves: OPREQ-208A-001\n\nREFUSE: not a registered trader.\n",
            block_text("OPREQ-208A-001", type_="external-action-authorization"),
        )
        self.assertIn("Status: REFUSED", out)
        self.assertNotIn("Status: RESOLVED", out)
        self.assertIn("Refusal recorded:", out)
        self.assertIn("not a registered trader", out)

    def test_refuse_works_without_an_authorization_block(self):
        # The whole point: someone declining to authorize cannot supply
        # System/Action/Target/Limit, and must not be asked to.
        out = self._refuse_run(
            "Resolves: OPREQ-208A-001\nREFUSE\n",
            block_text("OPREQ-208A-001", type_="external-action-authorization"),
        )
        self.assertIn("Status: REFUSED", out)

    def test_prose_mentioning_refusal_does_not_close_anything(self):
        out = self._refuse_run(
            "Resolves: OPREQ-208A-001\n\nI considered whether to REFUSE this and "
            "decided to authorize it instead.\n\n"
            "Authorization for OPREQ-208A-001:\nSystem: S\nAction: A\n"
            "Target: T\nLimit: L\n",
            block_text("OPREQ-208A-001", type_="external-action-authorization"),
        )
        self.assertNotIn("Status: REFUSED", out)
        self.assertIn("Status: RESOLVED", out)

    def test_bare_refuse_with_two_requests_fails_closed(self):
        out = self._refuse_run(
            "Resolves: OPREQ-208A-001\nResolves: OPREQ-215TFB-WTP-001\n\nREFUSE\n",
            block_text("OPREQ-208A-001", type_="external-action-authorization"),
            block_text("OPREQ-215TFB-WTP-001", type_="external-action-authorization"),
        )
        self.assertNotIn("REFUSED", out)
        audit = (self.app / "memories" / "operator-requests-audit.log").read_text()
        self.assertIn("REFUSE-AMBIGUOUS", audit)

    def test_named_refuse_targets_only_that_request(self):
        out = self._refuse_run(
            "Resolves: OPREQ-208A-001\nResolves: OPREQ-215TFB-WTP-001\n\n"
            "REFUSE OPREQ-215TFB-WTP-001 — sender identification cannot be satisfied.\n",
            block_text("OPREQ-208A-001", type_="external-action-authorization"),
            block_text("OPREQ-215TFB-WTP-001", type_="external-action-authorization"),
        )
        wtp = out[out.index("## OPREQ-215TFB-WTP-001"):]
        other = out[out.index("## OPREQ-208A-001"):out.index("## OPREQ-215TFB-WTP-001")]
        self.assertIn("Status: REFUSED", wtp)
        self.assertIn("Status: OPEN", other)

    # --- document-procurement: the operator writes the path where they were told to ---
    #
    # Every such request says "add a human-directive.md entry containing Resolves: <id>
    # and an Evidence files: field". The verifier read that field only from the request
    # block in operator-requests.md, so following the instruction as written left the
    # request OPEN. Both places are now read; the checksum and path confinement are
    # unchanged and are what actually gate this.

    def _evidence(self, req_id="OPREQ-208A-001", body=b"approved footer text"):
        d = self.app / "memories" / "operator-evidence" / req_id
        d.mkdir(parents=True, exist_ok=True)
        f = d / "footer.md"
        f.write_bytes(body)
        rel = f"memories/operator-evidence/{req_id}/footer.md"
        return rel, hashlib.sha256(body).hexdigest()

    def test_evidence_files_in_the_directive_resolves(self):
        rel, h = self._evidence()
        ok, msg = orn.verify_resolution(
            "OPREQ-208A-001",
            {"Type": "document-procurement", "Expected document class": "at least 1 file"},
            f"Resolves: OPREQ-208A-001\nEvidence files: {rel} sha256:{h}\n",
            self.app,
        )
        self.assertTrue(ok, msg)

    def test_evidence_files_in_the_request_block_still_resolves(self):
        rel, h = self._evidence()
        ok, msg = orn.verify_resolution(
            "OPREQ-208A-001",
            {
                "Type": "document-procurement",
                "Expected document class": "at least 1 file",
                "Evidence files": f"{rel} sha256:{h}",
            },
            "Resolves: OPREQ-208A-001\n",
            self.app,
        )
        self.assertTrue(ok, msg)

    def test_directive_entry_with_a_wrong_checksum_is_rejected(self):
        rel, _ = self._evidence()
        ok, msg = orn.verify_resolution(
            "OPREQ-208A-001",
            {"Type": "document-procurement"},
            f"Resolves: OPREQ-208A-001\nEvidence files: {rel} sha256:{'0' * 64}\n",
            self.app,
        )
        self.assertFalse(ok)

    def test_directive_entry_cannot_escape_the_evidence_directory(self):
        _, h = self._evidence()
        ok, msg = orn.verify_resolution(
            "OPREQ-208A-001",
            {"Type": "document-procurement"},
            f"Resolves: OPREQ-208A-001\nEvidence files: ../../etc/passwd sha256:{h}\n",
            self.app,
        )
        self.assertFalse(ok)
        self.assertIn("outside", msg)


if __name__ == "__main__":
    unittest.main()
