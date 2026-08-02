#!/usr/bin/env python3
"""Generate jcode's MCP config from the repo's .mcp.json.

Why this exists: jcode v0.64.2 does NOT read a project-local `.mcp.json` (measured
2026-07-31), and it speaks **stdio only** — an http/sse server configured with either
`type` or `transport` never connects. Both facts were found by live probing, not by
reading docs, and both silently produce a model with FEWER TOOLS rather than an error.
That is the dangerous shape: the loop would keep running and simply stop being able to
write Airtable or read Linear, and nothing would say so.

So this script rewrites the same server set into `~/.jcode/mcp.json`:

  * stdio servers (airtable, linear — the community npx packages the Claude engine
    already uses) pass through unchanged, so loop capability is identical to today's.
  * http servers (context7, browseros) are wrapped in the `mcp-remote` stdio bridge:
    `npx -y mcp-remote <url> --allow-http --transport http-only [--header "K: V"]`
    Verified PASS for both on 2026-07-31.

Env interpolation is done HERE, writing literal values, because `${VAR}` expansion
inside jcode's own config is unverified in this build — and an unexpanded key is an
auth failure that, again, degrades quietly. A referenced-but-unset variable makes the
server be SKIPPED with a loud line on stderr rather than written with a broken value.

Usage:
    jcode-mcp-config.py [--src .mcp.json] [--dest ~/.jcode/mcp.json] [--print]

Exit codes: 0 ok; 2 source unreadable/invalid; 3 every server was skipped (nothing
usable was produced — treat as a failed boot step, not a warning).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

# Per-server overrides applied ONLY on the jcode path, each with a measured reason.
# These are not preference: without them a provider is simply unusable.
# The set a cycle cannot work without. Writing a config that lacks any of these is a
# failure, not a degraded success: the loop would keep running and quietly stop being
# able to read or write the company's own state.
REQUIRED = ("airtable", "linear", "context7", "browseros")

OVERRIDES: dict[str, dict] = {
    # The community `@tacticlaunch/mcp-linear` package publishes a tool whose JSON
    # schema uses `contains` (linear_createManagedOAuthApplication.grantTypes). The
    # OpenAI API REJECTS THE WHOLE REQUEST on it — every openai-provider cycle dies
    # with `invalid_function_parameters` before doing any work (measured 2026-07-31).
    # Anthropic accepts the same schema, so this would have looked fine right up to
    # the first Codex-routed cycle after cutover. Linear's own hosted endpoint (the
    # one the Codex CLI already uses in production) does not carry that tool; a live
    # read of APP-272 through it on the openai provider returned the real title and
    # state, so write capability is preserved, not traded away.
    "linear": {
        "url": "https://mcp.linear.app/mcp",
        "headers": {"Authorization": "Bearer ${LINEAR_API_KEY}"},
        "_why": "community server's schema is rejected by the OpenAI API",
    },
    # The community `airtable-mcp-server` package does not start at all in the trixie
    # image: `Cannot find module 'hono/ws'` from its own dependency tree (measured
    # 2026-07-31). jcode reports no error for a server that fails to launch — the model
    # simply has no Airtable tools, which for this company is the single most-used write
    # surface. Airtable's hosted endpoint (already used by the Codex CLI in production)
    # starts cleanly through the same mcp-remote bridge; verified by listing bases from
    # inside a cycle and getting the real base name back.
    "airtable": {
        "url": "https://mcp.airtable.com/mcp",
        "headers": {"Authorization": "Bearer ${AIRTABLE_API_KEY}"},
        "_why": "community npx package fails to start (broken dep) and jcode reports no error",
    },
}


def expand(value: str) -> str | None:
    """Substitute ${VAR} from the environment. Returns None if any var is unset."""
    missing: list[str] = []

    def sub(m: re.Match[str]) -> str:
        got = os.environ.get(m.group(1))
        if not got:
            missing.append(m.group(1))
            return ""
        return got

    out = VAR_RE.sub(sub, value)
    return None if missing else out


def convert(name: str, spec: dict) -> tuple[dict | None, str]:
    """Return (jcode server spec, note). None means skip this server."""
    url = spec.get("url")
    is_http = bool(url) or spec.get("type") in ("http", "sse") or spec.get("transport")

    if not is_http:
        cmd, args = spec.get("command"), list(spec.get("args") or [])
        if not cmd:
            return None, "no command and no url"
        env_out: dict[str, str] = {}
        for k, v in (spec.get("env") or {}).items():
            got = expand(str(v))
            if got is None:
                return None, f"env {k} references an unset variable"
            env_out[k] = got
        out: dict = {"command": cmd, "args": args}
        if env_out:
            out["env"] = env_out
        return out, "stdio passthrough"

    # http/sse -> mcp-remote stdio bridge
    got_url = expand(str(url or ""))
    if not got_url:
        return None, "url missing or references an unset variable"
    # Prefer the image-installed binary; fall back to npx only if it is absent. The npx
    # path is the one that produced two silent, dependency-corrupt server failures.
    bridge = shutil.which("mcp-remote")
    if bridge:
        cmd_name, args = bridge, [got_url, "--allow-http", "--transport", "http-only"]
    else:
        cmd_name = "npx"
        args = ["-y", "mcp-remote", got_url, "--allow-http", "--transport", "http-only"]
    # Headers stay UNEXPANDED in argv. mcp-remote expands ${VAR} in --header values from
    # its own environment (README-documented, and proven behaviourally 2026-08-02: a local
    # sink received "Bearer sekret-canary-42" while the argv carried the literal
    # "Bearer ${AUTH_TOKEN}"). Expanding here put the real key on the command line, where
    # `ps` reads it — the exact shape that leaked three API keys on 2026-08-01. The value
    # rides in the child's env block instead; the probe and jcode both pass that through.
    env_out = {}
    for k, v in (spec.get("headers") or {}).items():
        v = str(v)
        for var in VAR_RE.findall(v):
            got = os.environ.get(var)
            if not got:
                return None, f"header {k} references unset variable {var}"
            env_out[var] = got
        args += ["--header", f"{k}: {v}"]
    out = {"command": cmd_name, "args": args}
    if env_out:
        out["env"] = env_out
    return (out,
            "http via mcp-remote bridge" + ("" if cmd_name == "npx" else " (image-installed)"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="/app/.mcp.json")
    ap.add_argument("--dest", default=str(Path.home() / ".jcode" / "mcp.json"))
    ap.add_argument("--print", action="store_true",
                    help="print the result with secrets masked; write nothing")
    args = ap.parse_args()

    try:
        src = json.loads(Path(args.src).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"cannot read {args.src}: {e}", file=sys.stderr)
        return 2

    servers = src.get("mcpServers") or {}
    if not servers:
        print(f"{args.src} has no mcpServers", file=sys.stderr)
        return 2

    out: dict[str, dict] = {}
    for name, spec in servers.items():
        spec = spec if isinstance(spec, dict) else {}
        if name in OVERRIDES:
            ov = dict(OVERRIDES[name])
            why = ov.pop("_why", "")
            print(f"[jcode-mcp] override {name}: {why}", file=sys.stderr)
            spec = ov
        conv, note = convert(name, spec)
        if conv is None:
            print(f"[jcode-mcp] SKIP {name}: {note}", file=sys.stderr)
            continue
        out[name] = conv
        print(f"[jcode-mcp] ok   {name}: {note}", file=sys.stderr)

    if not out:
        print("[jcode-mcp] no usable servers — refusing to write an empty config",
              file=sys.stderr)
        return 3

    payload = {"mcpServers": out}

    if args.print:
        masked = json.loads(json.dumps(payload))
        for s in masked["mcpServers"].values():
            s["args"] = [re.sub(r"(: ).+", r"\1***", a) for a in s.get("args", [])]
            if "env" in s:
                s["env"] = {k: "***" for k in s["env"]}
        print(json.dumps(masked, indent=2))
        return 0

    missing = [n for n in REQUIRED if n not in out]
    if missing:
        print(f"[jcode-mcp] REQUIRED server(s) missing from the result: {','.join(missing)} — "
              "refusing to write a partial config", file=sys.stderr)
        return 3

    dest = Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    # Write to a temp file in the SAME directory, then rename. rename(2) is atomic, so a
    # reader (jcode starting a cycle) sees either the previous complete config or the
    # new complete one — never a half-written file that would parse as "fewer servers"
    # and silently produce a tool-less cycle. O_TRUNC on the real path could do exactly
    # that if the process died mid-write.
    tmp = dest.with_name(dest.name + f".tmp.{os.getpid()}")
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, 0o600)   # explicit: O_CREAT honours umask, and a pre-existing
                               # file's looser mode would otherwise survive
        os.replace(tmp, dest)
    except OSError as e:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        print(f"[jcode-mcp] cannot write {dest}: {e}", file=sys.stderr)
        return 3
    # Freshness stamp (REVISE-2 gate B11). JCODE_HOME is a persistent volume, so a
    # STALE mcp.json from a previous boot survives a failed generation and would
    # pass every content check. The stamp records WHEN this exact bytes-on-disk
    # config was produced; the loop's boot gate requires epoch >= container boot
    # AND a matching sha256, so "generation failed this boot" is caught even when
    # yesterday's config looks perfect. Same atomic write discipline.
    meta = dest.with_name(dest.name + ".meta")
    sha = hashlib.sha256(dest.read_bytes()).hexdigest()
    mtmp = meta.with_name(meta.name + f".tmp.{os.getpid()}")
    try:
        fd = os.open(mtmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump({"epoch": int(time.time()), "sha256": sha,
                       "servers": sorted(out)}, fh)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(mtmp, meta)
    except OSError as e:
        try:
            os.unlink(mtmp)
        except OSError:
            pass
        print(f"[jcode-mcp] cannot write freshness stamp {meta}: {e} — "
              "the boot gate will treat this generation as FAILED", file=sys.stderr)
        return 3
    print(f"[jcode-mcp] wrote {len(out)} servers -> {dest} (atomic, stamped {sha[:12]})",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
