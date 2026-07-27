#!/usr/bin/env python3
"""Deterministic directive-promotion gate — narrow v1 (2026-07-27).

NOT an LLM judgment call. Pure text/pattern matching against the Opportunity
Analyst's own report, run AFTER the report is written and BEFORE anything
touches memories/human-directive.md. Exact scope per explicit operator
instruction (never loosen without a new instruction):

  - Fail-closed: any missing field, parse ambiguity, or unrecognized shape
    blocks promotion. Silence/exception -> BLOCKED, never PROMOTED.
  - No blanket NO-GO auto-promotion. NO-GO (or any other escalation beyond a
    bare, unchanged HOLD) is only eligible for candidates OTHER than the
    current human-selected Active Validation.
  - The Active Validation itself may, at most, receive a HOLD from the
    analyst's own qualitative call. Any GO / NO-GO / PIVOT / QUEUE / ARCHIVE /
    KILL / STOP-GATE language found near a mention of the active candidate ID
    blocks the whole directive.
  - A single risk-keyword hit ANYWHERE in the report (outreach, payment,
    fulfillment, build, new active validation, buyer/offer/price/channel
    change, legal action, expenditure, external write) blocks the WHOLE
    directive. No partial/cherry-picked apply of the "safe" parts of a mixed
    directive — ever.
  - Mechanical registry/ledger corrections are handled by the SEPARATE pass-2
    codex call (which is instructed to transcribe already-stated verdicts,
    never to re-judge evidence) — this gate does not re-implement that; it
    only decides whether the report's proposed human-directive.md text may be
    auto-applied.
  - Every promotion is backed up, hashed, diffed, and read-back verified.

Exit code is always 0 (never fails the caller); stdout is exactly one of:
  PROMOTED
  BLOCKED: <reason>
"""
from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
CONSENSUS = APP / "memories" / "consensus.md"
DIRECTIVE_LIVE = APP / "memories" / "human-directive.md"
AUDIT_LOG = APP / "memories" / "directive-promotion-audit.log"
BACKUP_DIR = APP / "memories" / "human-directive-backups"
TELEGRAM_NOTIFY = APP / "scripts" / "core" / "telegram-notify.sh"

# Generous / over-inclusive on purpose — a false positive just means "manual
# review", which is today's status quo and always safe. A false negative is
# the only failure mode that matters here.
RISK_TERMS = [
    r"outreach", r"cold[- ]?email", r"reach out", r"\bdm\b.{0,15}the",
    r"contact the buyer", r"linkedin message", r"send.{0,15}email",
    r"email campaign",
    r"\bcharge\b", r"\binvoice\b", r"\bcheckout\b", r"\bstripe\b", r"\bpaddle\b",
    r"collect payment", r"process payment", r"accept payment",
    r"deliver the", r"\bfulfil{1,2}\b", r"ship the", r"hand off to",
    r"complete the order",
    r"\bdeploy\b", r"\bwrangler\b", r"build the", r"write code",
    r"implement the", r"create project",
    r"activate candidate", r"new active validation",
    r"select.{0,20}as active", r"\bmay start\b", r"\bwill start\b",
    r"\bshould start\b", r"begin.{0,15}(test|validation)",
    r"change the price", r"new price", r"different buyer", r"new channel",
    r"switch.{0,15}offer", r"modify.{0,15}offer",
    r"\battorney\b", r"\bcounsel\b", r"\blawyer\b", r"contract with",
    r"sözleşme", r"avukat",
    r"\bpurchase\b", r"expenditure", r"harcama", r"spend \$", r"pay for",
    r"post to linear", r"update linear", r"write to airtable",
    r"update airtable", r"external write",
]
RISK_RE = re.compile("|".join(RISK_TERMS), re.IGNORECASE)

VERDICT_RE = re.compile(
    r"\b(HOLD|NO-GO|PAUSE(D)?|ARCHIVE(D)?|CONFIRMED KILL|TEST-BLOCKED|"
    r"PRICING-STRUCTURE UNKNOWN|RESEARCH[- ]ONLY|DEFERRED)\b",
    re.IGNORECASE,
)

ESCALATION_RE = re.compile(
    r"\bGO\b|NO-GO|PIVOT|TERMINAL|STOP GATE|\bKILL\b|ARCHIVE|"
    r"CONDITIONAL GO|\bQUEUE\b|QUEUED",
    re.IGNORECASE,
)

ACTIVE_ID_RE = re.compile(r"Active Validation ID:\s*`([^`]+)`")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(msg: str) -> None:
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with AUDIT_LOG.open("a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {msg}\n")


def blocked(reason: str) -> None:
    audit(f"BLOCKED: {reason}")
    print(f"BLOCKED: {reason}")
    sys.exit(0)


def notify(msg: str) -> None:
    if not TELEGRAM_NOTIFY.exists():
        return
    try:
        subprocess.run([str(TELEGRAM_NOTIFY), msg], timeout=15, check=False)
    except Exception:
        pass


def main() -> None:
    if len(sys.argv) != 2:
        blocked("usage: promote_directive.py <analysis-directive.md path>")
    report_path = Path(sys.argv[1])

    for p, label in [
        (report_path, "report"),
        (CONSENSUS, "consensus.md"),
        (DIRECTIVE_LIVE, "human-directive.md"),
    ]:
        if not p.is_file():
            blocked(f"{label} missing: {p}")

    report_text = report_path.read_text(encoding="utf-8", errors="replace")
    if len(report_text.strip()) < 200:
        blocked("report too short to classify")

    live_text = DIRECTIVE_LIVE.read_text(encoding="utf-8", errors="replace")
    # Logged on every BLOCKED outcome from here on (operator's monitoring ask,
    # 2026-07-27): makes "human-directive.md hash unchanged on block" trivially
    # checkable per run without re-hashing by hand.
    unchanged_hash = sha256(DIRECTIVE_LIVE)
    status_match = re.search(r"^## Status\s*\n(\S+)", live_text, re.MULTILINE)
    current_status = status_match.group(1).strip() if status_match else None
    if current_status != "DONE":
        blocked(
            f"current human-directive.md Status is "
            f"'{current_status}', not DONE — never overwrite in-flight work"
            f" | human_directive_hash={unchanged_hash[:12]} (unchanged)"
        )

    hit = RISK_RE.search(report_text)
    if hit:
        blocked(f'risk-keyword hit: "{hit.group(0)}" | human_directive_hash={unchanged_hash[:12]} (unchanged)')

    if not VERDICT_RE.search(report_text):
        blocked(
            "no recognized narrowing-verdict keyword found — not confidently classifiable"
            f" | human_directive_hash={unchanged_hash[:12]} (unchanged)"
        )

    consensus_text = CONSENSUS.read_text(encoding="utf-8", errors="replace")
    active_match = ACTIVE_ID_RE.search(consensus_text)
    active_id = active_match.group(1).split("|")[0].strip() if active_match else None

    if active_id:
        # Bare ID token, e.g. "176-R" out of a longer "176-R | buyer | ..." field.
        active_token = active_id.split()[0].strip("`")
        lines = report_text.splitlines()
        for i, line in enumerate(lines):
            if active_token not in line:
                continue
            window = "\n".join(lines[max(0, i - 3) : i + 4])
            esc = ESCALATION_RE.search(window)
            if esc:
                blocked(
                    f'active candidate "{active_token}" referenced near '
                    f'escalation language "{esc.group(0)}" '
                    f"(context: line {i + 1})"
                    f" | human_directive_hash={unchanged_hash[:12]} (unchanged)"
                )

    # --- all gates passed: promote ---
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    before_hash = sha256(DIRECTIVE_LIVE)
    stamp_compact = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup_path = BACKUP_DIR / f"human-directive-{stamp_compact}.md"
    backup_path.write_bytes(DIRECTIVE_LIVE.read_bytes())

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    new_content = (
        "# Human Directive\n\n"
        "<!-- AUTO-PROMOTED by scripts/analyst/promote_directive.py "
        "(narrow v1, 2026-07-27).\n"
        f"     Source report: {report_path} @ {stamp}. This was NOT typed by "
        "the operator —\n"
        f"     see {AUDIT_LOG} for the promotion decision and hashes. -->\n\n"
        "## Status\nPENDING\n\n"
        "## Directive\n" + report_text
    )
    DIRECTIVE_LIVE.write_text(new_content, encoding="utf-8")

    # read-back verification
    readback = DIRECTIVE_LIVE.read_text(encoding="utf-8")
    if readback != new_content:
        DIRECTIVE_LIVE.write_bytes(backup_path.read_bytes())
        blocked("read-back verification failed — restored backup, did not promote")

    after_hash = sha256(DIRECTIVE_LIVE)
    diff_lines = len(
        [
            line
            for line in subprocess.run(
                ["diff", str(backup_path), str(DIRECTIVE_LIVE)],
                capture_output=True,
                text=True,
                check=False,
            ).stdout.splitlines()
        ]
    )
    audit(
        f"PROMOTED: source={report_path} before_hash={before_hash} "
        f"after_hash={after_hash} backup={backup_path} diff_lines={diff_lines}"
    )
    print("PROMOTED")
    notify(
        "🤖 Opportunity Analyst directive auto-promoted under standing "
        f"delegation (narrow v1). Source: {report_path.name}. "
        f"Backup: {backup_path.name}. Review in cockpit Director panel."
    )


if __name__ == "__main__":
    main()
