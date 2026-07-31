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
import json
import os
import re
import sys
from pathlib import Path

VAR_RE = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")


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
    args = ["-y", "mcp-remote", got_url, "--allow-http", "--transport", "http-only"]
    for k, v in (spec.get("headers") or {}).items():
        got = expand(str(v))
        if got is None:
            return None, f"header {k} references an unset variable"
        args += ["--header", f"{k}: {got}"]
    return {"command": "npx", "args": args}, "http via mcp-remote bridge"


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
        conv, note = convert(name, spec if isinstance(spec, dict) else {})
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

    dest = Path(args.dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    # 0600: the file holds API keys in cleartext, same as CODEX_HOME/auth.json.
    fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print(f"[jcode-mcp] wrote {len(out)} servers -> {dest}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
