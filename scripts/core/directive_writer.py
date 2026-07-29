#!/usr/bin/env python3
"""The ONE way `memories/human-directive.md` is written.

Five writers used to touch this file, each its own way, none of them locking and
only one refusing to clobber in-flight work. On 2026-07-29 a census found the
worst of them — the analyst's snapshot/restore — able to silently revert an
operator's PENDING instruction for up to ~50 minutes, logged under a message that
described the opposite of what it did. Backing the file up first would have made
that loss recoverable; it would not have stopped it happening.

So every write goes through this pipeline, operator-specified:

    lock → read current status+hash → in-flight gate → persistent backup
    → temp file → atomic rename → read-back + hash verify → audit → notify

Two rules the pipeline exists to enforce, both of them fail-closed:

  * **In-flight work is not clobbered.** A PENDING directive is a live
    instruction. Overwriting it needs `--allow-pending`, which is a choice
    someone makes, not a default.
  * **The body is immutable after acceptance.** The only permitted change to an
    accepted directive is its `## Status` value, and only via `status`, which is
    a compare-and-swap: it verifies the body is byte-identical to what the caller
    was given before it moves anything. A model must never write this file; it
    produces a receipt and calls this.

Subcommands
  write   --body-file F [--allow-pending] [--actor NAME]
  status  --expect-status S --to S2 --expect-body-sha256 H [--receipt F]
  restore --from-file SNAP --expect-sha256 H [--actor NAME]
  show

Exit codes: 0 ok · 2 refused by a gate (in-flight, hash mismatch) · 3 I/O or
verification failure. A refusal is a normal outcome and says why on stderr.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

APP = Path(os.environ.get("AC_APP_DIR", "/app"))
DIRECTIVE = APP / "memories" / "human-directive.md"
BACKUPS = APP / "memories" / "human-directive-backups"
RECOVERY = APP / "memories" / "human-directive-recovery"
AUDIT = APP / "memories" / "directive-audit.log"
LOCK = APP / "memories" / ".human-directive.lock"
NOTIFY = APP / "scripts" / "core" / "telegram-notify.sh"

STATUS_RE = re.compile(r"^## Status\s*\n(\S+)\s*$", re.MULTILINE)


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_live() -> tuple[str, str, str]:
    """(text, sha256, status) — empty strings when the file is absent."""
    if not DIRECTIVE.exists():
        return "", "", ""
    text = DIRECTIVE.read_text(encoding="utf-8")
    m = STATUS_RE.search(text)
    return text, sha(text), (m.group(1) if m else "")


def body_of(text: str) -> str:
    """Everything except the Status VALUE — what must not change on a transition.

    The status line is normalized to a placeholder rather than deleted, so a
    caller cannot smuggle a body edit past the comparison by also deleting the
    heading.
    """
    return STATUS_RE.sub("## Status\n\x00", text)


def audit(action: str, actor: str, before: str, after: str, detail: str) -> None:
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    line = (f"{now()}\taction={action}\tactor={actor}"
            f"\tbefore_sha={before[:16] or '-'}\tafter_sha={after[:16] or '-'}\t{detail}\n")
    with AUDIT.open("a", encoding="utf-8") as fh:
        fh.write(line)


def notify(msg: str) -> None:
    if not (os.environ.get("TELEGRAM_BOT_TOKEN") and os.environ.get("TELEGRAM_CHAT_ID")):
        return
    if not NOTIFY.exists():
        return
    try:
        subprocess.run(["bash", str(NOTIFY), msg], capture_output=True, timeout=25)
    except Exception:  # noqa: BLE001 — a failed notification must never fail a write
        pass


def backup(text: str, reason: str) -> Path | None:
    """Persist the about-to-be-destroyed content. Failure here BLOCKS the write.

    Ordered before the write on purpose: believing you have recoverability you do
    not have is worse than knowing you have none.
    """
    if not text:
        return None
    BACKUPS.mkdir(parents=True, exist_ok=True)
    p = BACKUPS / f"human-directive-{now().replace(':', '')}-{reason}.md"
    p.write_text(text, encoding="utf-8")
    if p.read_text(encoding="utf-8") != text:
        raise OSError(f"backup verify failed: {p}")
    return p


def atomic_write(text: str) -> None:
    DIRECTIVE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(DIRECTIVE.parent), prefix=".hd-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, DIRECTIVE)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def verify_written(expected: str) -> str:
    back = DIRECTIVE.read_text(encoding="utf-8")
    if back != expected:
        raise OSError("read-back mismatch: the file on disk is not what was written")
    return sha(back)


class Refused(Exception):
    """A gate said no. Not an error — the point of the gate."""


def with_lock(fn):
    def wrapper(*a, **kw):
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        with LOCK.open("w") as lk:
            fcntl.flock(lk, fcntl.LOCK_EX)
            try:
                return fn(*a, **kw)
            finally:
                fcntl.flock(lk, fcntl.LOCK_UN)
    return wrapper


HEADER = (
    "# Human Directive\n\n"
    "<!-- Written by scripts/core/directive_writer.py — the only writer. Do NOT\n"
    "     hand-edit and do NOT let a model edit this file: the body is immutable\n"
    "     after acceptance, and PENDING->DONE goes through `directive_writer.py\n"
    "     status`, which compare-and-swaps on the body hash. -->\n\n"
)


@with_lock
def cmd_write(args) -> int:
    body = Path(args.body_file).read_text(encoding="utf-8").rstrip() + "\n"
    if not body.strip():
        print("refused: empty directive body", file=sys.stderr)
        return 2
    live, live_sha, live_status = read_live()

    if live_status == "PENDING" and not args.allow_pending:
        print("refused: the live directive is PENDING — that is in-flight work.\n"
              "         Pass --allow-pending to overwrite it deliberately.",
              file=sys.stderr)
        audit("write-refused", args.actor, live_sha, "", "reason=in-flight-pending")
        notify(f"🚧 Directive write REFUSED ({args.actor}): live directive is PENDING, not overwritten.")
        return 2

    bk = backup(live, "preoverwrite")
    new = f"{HEADER}## Status\nPENDING\n\n## Updated\n{now()}\n\n## Directive\n{body}"
    atomic_write(new)
    new_sha = verify_written(new)
    audit("write", args.actor, live_sha, new_sha,
          f"backup={bk.name if bk else '-'} allow_pending={args.allow_pending}")
    print(f"ok: directive written, status=PENDING sha256={new_sha[:16]} "
          f"backup={bk.name if bk else '(none — no previous file)'}")
    return 0


@with_lock
def cmd_status(args) -> int:
    """Compare-and-swap the Status value. The body must be untouched."""
    live, live_sha, live_status = read_live()
    if not live:
        print("refused: no directive file", file=sys.stderr)
        return 2
    if live_status != args.expect_status:
        print(f"refused: status is {live_status!r}, expected {args.expect_status!r} — "
              "someone else moved it", file=sys.stderr)
        audit("status-refused", args.actor, live_sha, "",
              f"want_from={args.expect_status} found={live_status}")
        return 2
    got_body = sha(body_of(live))
    if got_body != args.expect_body_sha256:
        print(f"refused: body hash {got_body[:16]} != expected "
              f"{args.expect_body_sha256[:16]} — the directive changed under you.\n"
              "         The body is immutable after acceptance; nothing was written.",
              file=sys.stderr)
        audit("status-refused", args.actor, live_sha, "", "reason=body-hash-mismatch")
        notify("🚧 Directive status transition REFUSED: body hash mismatch — "
               "the directive changed mid-execution. Nothing written.")
        return 2

    bk = backup(live, f"status-{args.expect_status}-to-{args.to}")
    new = STATUS_RE.sub(f"## Status\n{args.to}", live, count=1)
    if body_of(new) != body_of(live):
        print("refused: transition would alter the body — refusing", file=sys.stderr)
        return 2
    atomic_write(new)
    new_sha = verify_written(new)
    receipt = args.receipt or "-"
    audit("status", args.actor, live_sha, new_sha,
          f"{args.expect_status}->{args.to} receipt={receipt} backup={bk.name if bk else '-'}")
    print(f"ok: status {args.expect_status} -> {args.to} sha256={new_sha[:16]}")
    return 0


@with_lock
def cmd_restore(args) -> int:
    """The analyst path: put a snapshot back ONLY if nothing else has written.

    Backing up first would make a clobber recoverable; this refuses to clobber.
    If the live file moved since the snapshot was taken, the snapshot is stale by
    definition — someone with more right to the slot wrote it — so the restore
    candidate goes to a recovery file and the live file is left alone.
    """
    snap = Path(args.from_file).read_text(encoding="utf-8")
    live, live_sha, live_status = read_live()

    if live_sha == sha(snap):
        print("ok: live file identical to snapshot, nothing to restore")
        return 0

    if live_sha != args.expect_sha256:
        RECOVERY.mkdir(parents=True, exist_ok=True)
        cand = RECOVERY / f"restore-candidate-{now().replace(':', '')}.md"
        cand.write_text(snap, encoding="utf-8")
        print("refused: the live directive changed since the snapshot was taken "
              f"(live {live_sha[:16]}, expected {args.expect_sha256[:16]}).\n"
              f"         Someone else wrote it — status={live_status or 'unknown'}. "
              "Live file untouched.\n"
              f"         Restore candidate saved: {cand}", file=sys.stderr)
        audit("restore-refused", args.actor, live_sha, "",
              f"expected={args.expect_sha256[:16]} candidate={cand.name} live_status={live_status}")
        notify("🚧 Analyst restore REFUSED — the directive was written by someone else "
               f"during the analyst run (status={live_status or 'unknown'}). Live file "
               f"untouched; candidate kept at {cand.name}.")
        return 2

    bk = backup(live, "prerestore")
    atomic_write(snap)
    new_sha = verify_written(snap)
    audit("restore", args.actor, live_sha, new_sha, f"backup={bk.name if bk else '-'}")
    print(f"ok: snapshot restored sha256={new_sha[:16]}")
    return 0


def cmd_show(args) -> int:
    live, live_sha, live_status = read_live()
    print(f"status={live_status or '(none)'}")
    print(f"file_sha256={live_sha or '(none)'}")
    print(f"body_sha256={sha(body_of(live)) if live else '(none)'}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--actor", default=os.environ.get("AC_ACTOR", "unknown"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("write"); w.set_defaults(fn=cmd_write)
    w.add_argument("--body-file", required=True)
    w.add_argument("--allow-pending", action="store_true")

    s = sub.add_parser("status"); s.set_defaults(fn=cmd_status)
    s.add_argument("--expect-status", required=True)
    s.add_argument("--to", required=True)
    s.add_argument("--expect-body-sha256", required=True)
    s.add_argument("--receipt")

    r = sub.add_parser("restore"); r.set_defaults(fn=cmd_restore)
    r.add_argument("--from-file", required=True)
    r.add_argument("--expect-sha256", required=True)

    sub.add_parser("show").set_defaults(fn=cmd_show)

    # baseline / reconcile are NOT operations of this protocol, by design
    # (operator mandate, 2026-07-29): the agent must never be able to bless a
    # hash mismatch it may itself have caused. Reconciliation and baselining
    # happen ONLY through the operator's host-side channel
    # (autocompany-deploy/scripts/directive-baseline.sh), outside the container.
    # Registering them here as hard refusals makes the boundary explicit instead
    # of an argparse "invalid choice" that reads like a missing feature.
    def _refuse_forbidden(name: str):
        def fn(_args) -> int:
            raise Refused(
                f"'{name}' is not an operation of this writer and never will be: "
                "baselining/reconciling the audit ledger is operator-only, via the "
                "host-side directive-baseline.sh channel outside the container")
        return fn

    for _forbidden in ("baseline", "reconcile"):
        sub.add_parser(_forbidden).set_defaults(fn=_refuse_forbidden(_forbidden))

    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
