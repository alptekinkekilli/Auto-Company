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
    normalize_ownership(AUDIT)


def _telegram_env() -> dict[str, str]:
    """Telegram creds, from the process env or — failing that — runtime.env.

    The writer is invoked three ways: by the dashboard (a child of the entrypoint, so
    the env is there), by `docker exec` from apply-directive.sh, and by the analyst.
    A `docker exec` gets a FRESH shell that never sourced runtime.env, so both vars are
    empty and notify() returned silently — measured 2026-08-01: every refusal on the
    apply-directive.sh path was invisible to the operator, including the in-flight gate
    firing on a directive they believed had been applied. Read the file as a fallback so
    the alerting does not depend on which door the writer came through.
    """
    env = {k: os.environ.get(k, "") for k in ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID")}
    if all(env.values()):
        return env
    try:
        for line in open(APP / "logs" / "runtime.env", encoding="utf-8", errors="replace"):
            if "=" not in line or line.lstrip().startswith("#"):
                continue
            k, _, v = line.strip().partition("=")
            if k in env and not env[k]:
                env[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return env


def notify(msg: str) -> None:
    env = _telegram_env()
    if not all(env.values()):
        return
    if not NOTIFY.exists():
        return
    try:
        subprocess.run(["bash", str(NOTIFY), msg], capture_output=True, timeout=25,
                       env={**os.environ, **env})
    except Exception:  # noqa: BLE001 — a failed notification must never fail a write
        pass


def _why_pending(live_text: str) -> str:
    """A compact 'why is the live one still PENDING' for the refusal notification.

    Operator feedback 2026-08-01: the refusal told them WHAT happened but not why the
    slot was occupied, so a directive they believed applied sat unexplained for 31h.
    The honest answer is the directive's OWN Completion clause — the conditions it set
    for itself — plus how long it has been waiting. Quoted, never paraphrased: a
    summary of a completion condition is how a gate gets softened by accident.
    """
    import re as _re
    from datetime import datetime as _dt, timezone as _tz

    age = ""
    m = _re.search(r"^##\s*Updated\s*\n+(\S+)", live_text, _re.MULTILINE)
    if m:
        try:
            then = _dt.fromisoformat(m.group(1).strip().replace("Z", "+00:00"))
            age = f" for {(_dt.now(_tz.utc) - then).total_seconds() / 3600:.1f}h"
        except ValueError:
            pass

    body = ""
    m2 = _re.search(r"^##\s*Completion\s*$(.+?)(?=^##\s|\Z)", live_text,
                    _re.MULTILINE | _re.DOTALL)
    if m2:
        body = " ".join(m2.group(1).split())
        if len(body) > 700:
            body = body[:700].rsplit(" ", 1)[0] + " …"
    return age, body


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
    normalize_ownership(p)
    return p


def normalize_ownership(p: Path) -> None:
    """Make the file readable by the loop/dashboard user regardless of invoker.

    The writer is exec'd through more than one identity: the dashboard runs it as
    `app`, but the operator's host-side channel reaches it via `docker exec`,
    whose default user is root on this image. mkstemp creates 0600 files owned by
    the invoker, and os.replace carries that onto the live slot — measured
    2026-07-29: a root-invoked write left human-directive.md root:root 0600, the
    app-uid loop could not even hash it, and the cockpit showed an empty PENDING.
    So after every write, chown to the memories directory's owner (the app user)
    and open the mode to 0644. chown needs root; when the invoker IS the app
    user the file is already right, so failure here is fine to ignore.

    TEMPORARY OWNERSHIP COMPATIBILITY (operator mandate, verbatim, 2026-07-29):

        The current `normalize_ownership()` behavior is a pre-isolation
        compatibility fix only. It MUST NOT preserve `app:app` ownership after
        OS isolation.

        During migration:

        - canonical directive, audit ledger, backups, and recovery artifacts
          must remain owned by the dedicated writer UID;
        - uid 10001 may receive read access only;
        - the protected parent directory must not permit uid 10001 to replace,
          rename, or unlink files;
        - a root-invoked operator write must preserve writer-UID ownership
          rather than converting protected files back to app ownership;
        - production acceptance tests must verify ownership and EPERM again
          after both an agent status transition and a host/root operator write.

    In other words: this function chowns to the *directory owner*, and today the
    memories directory is owned by `app`. When the isolation lands, the protected
    directory's owner becomes the writer UID — at that point this function must
    follow it (it already will, since it stats the parent), and any hardcoded
    notion of "app owns these files" would silently undo the isolation. Do not
    add one.
    """
    try:
        st = os.stat(DIRECTIVE.parent)
        os.chown(p, st.st_uid, st.st_gid)
    except (PermissionError, OSError):
        pass
    try:
        os.chmod(p, 0o644)
    except OSError:
        pass


def atomic_write(text: str) -> None:
    DIRECTIVE.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(DIRECTIVE.parent), prefix=".hd-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
            fh.flush()
            os.fsync(fh.fileno())
        normalize_ownership(Path(tmp))
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
        _age, _completion = _why_pending(live)
        _msg = (
            f"🚧 Directive NOT applied ({args.actor}).\n\n"
            "Your new directive was REFUSED and nothing was written — the live "
            f"directive has been PENDING{_age} and is unchanged. This is the "
            "in-flight gate, not an error.\n\n"
        )
        if _completion:
            _msg += f"WHY IT IS STILL PENDING — its own Completion clause:\n{_completion}\n\n"
        _msg += (
            "To replace it deliberately:\n"
            "AC_ALLOW_PENDING=1 apply-directive.sh <file>\n\n"
            "Or close the live one first: directive_writer.py status (PENDING->DONE)."
        )
        notify(_msg)
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
