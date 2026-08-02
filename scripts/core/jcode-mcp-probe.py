#!/usr/bin/env python3
"""Deterministic MCP boot probe (REVISE-2 gates B8-B10).

Replaces the model-based probe: this speaks the MCP protocol itself — spawn each
server command from the generated mcp.json, JSON-RPC over stdio (newline-delimited),
initialize -> tools/list -> one read-only tools/call — and judges ONLY protocol-level
facts. No model run, no Claude quota, no prose to grade.

Checks, all fail-closed:
  1. config servers  == manifest servers, exactly (missing AND extra both fail)
  2. every server answers initialize + tools/list within the timeout
  3. live destructive tools (name matches the pattern) == manifest destructive
     list, exactly (an EXTRA destructive tool upstream fails the boot until the
     manifest AND the denylist are updated; a MISSING one means a stale manifest
     or the wrong endpoint answered)
  4. JCODE_TOOLS_DENY covers every manifest destructive tool (full
     mcp__<server>__<tool> name) and every manifest base_denied entry
  5. the manifest readcheck call returns a result with no protocol-level
     isError and content that does not begin with an error string

Writes a machine-readable evidence file (per-server tool census + readcheck
verdict) for the canary audit.

Exit: 0 all pass · 1 mismatch/unreachable · 2 probe could not run at all.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import select
import subprocess
import sys
import time

DESTRUCTIVE_RE = re.compile(r"(delete|remove|archive|revert|drop|destroy|purge)", re.I)
PROTOCOL_VERSION = "2025-06-18"


class ServerError(Exception):
    pass


class StdioClient:
    """Minimal MCP stdio client: newline-delimited JSON-RPC 2.0."""

    def __init__(self, name: str, command: str, args: list[str],
                 env: dict[str, str] | None, timeout: float):
        self.name = name
        self.deadline = time.monotonic() + timeout
        full_env = dict(os.environ)
        if env:
            full_env.update(env)
        try:
            self.proc = subprocess.Popen(
                [command] + list(args),
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, env=full_env)
        except OSError as e:
            raise ServerError(f"cannot spawn '{command}': {e}") from e
        self._buf = b""
        self._id = 0

    def _remaining(self) -> float:
        left = self.deadline - time.monotonic()
        if left <= 0:
            raise ServerError("timeout")
        return left

    def _send(self, obj: dict) -> None:
        data = (json.dumps(obj) + "\n").encode()
        try:
            self.proc.stdin.write(data)
            self.proc.stdin.flush()
        except (BrokenPipeError, OSError) as e:
            raise ServerError(f"server closed stdin ({e})") from e

    def _read_msg(self) -> dict:
        fd = self.proc.stdout.fileno()
        while True:
            nl = self._buf.find(b"\n")
            if nl >= 0:
                line, self._buf = self._buf[:nl], self._buf[nl + 1:]
                line = line.strip()
                if not line:
                    continue
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue  # log noise on stdout — skip, keep reading
            r, _, _ = select.select([fd], [], [], min(self._remaining(), 1.0))
            if not r:
                if self.proc.poll() is not None:
                    raise ServerError(f"server exited rc={self.proc.returncode}")
                continue
            chunk = os.read(fd, 65536)
            if not chunk:
                raise ServerError("server closed stdout")
            self._buf += chunk

    def request(self, method: str, params: dict | None = None) -> dict:
        self._id += 1
        rid = self._id
        self._send({"jsonrpc": "2.0", "id": rid, "method": method,
                    "params": params or {}})
        while True:
            msg = self._read_msg()
            if msg.get("id") == rid:
                if "error" in msg:
                    raise ServerError(f"{method} -> error: "
                                      f"{json.dumps(msg['error'])[:300]}")
                return msg.get("result") or {}
            # server-initiated notifications/requests: ignore

    def notify(self, method: str, params: dict | None = None) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def initialize(self) -> None:
        self.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "autocompany-boot-probe", "version": "2.0"},
        })
        self.notify("notifications/initialized")

    def list_tools(self) -> list[dict]:
        tools, cursor = [], None
        while True:
            params = {"cursor": cursor} if cursor else {}
            res = self.request("tools/list", params)
            tools.extend(res.get("tools") or [])
            cursor = res.get("nextCursor")
            if not cursor:
                return tools

    def call_tool(self, name: str, arguments: dict) -> dict:
        return self.request("tools/call", {"name": name, "arguments": arguments})

    def close(self) -> None:
        for f in (self.proc.stdin, self.proc.stdout):
            try:
                f.close()
            except OSError:
                pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


def probe_server(name: str, spec: dict, timeout: float) -> dict:
    cli = StdioClient(name, spec["command"], spec.get("args") or [],
                      spec.get("env"), timeout)
    try:
        cli.initialize()
        tools = cli.list_tools()
        names = sorted(t.get("name", "") for t in tools)
        return {"client": cli, "tools": names}
    except ServerError:
        cli.close()
        raise


def judge_readcheck(result: dict) -> str:
    """'' if the call is a genuine success, else the failure reason.

    Protocol-level only (gate B10): the isError flag, and content whose first
    text block BEGINS with an error string — never anything a model said.
    """
    if result.get("isError"):
        return "isError=true"
    content = result.get("content")
    if not content or not isinstance(content, list):
        return "empty content"
    first = content[0] if isinstance(content[0], dict) else {}
    text = str(first.get("text") or "")
    if re.match(r"\s*(error|failed|exception|unauthorized|forbidden)\b", text, re.I):
        return f"content begins with an error string: {text[:120]!r}"
    return ""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="generated jcode mcp.json")
    ap.add_argument("--manifest", required=True, help="operator-owned manifest")
    ap.add_argument("--evidence", default="", help="write evidence JSON here")
    ap.add_argument("--timeout", type=float,
                    default=float(os.environ.get("JCODE_PROBE_TIMEOUT", "90")))
    args = ap.parse_args()

    try:
        cfg = json.load(open(args.config, encoding="utf-8"))
        man = json.load(open(args.manifest, encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"MCP_PROBE_FAILED: cannot read config/manifest: {e}", file=sys.stderr)
        return 2

    cfg_servers = cfg.get("mcpServers") or {}
    man_servers = man.get("servers") or {}
    if not isinstance(cfg_servers, dict) or not isinstance(man_servers, dict) \
            or not man_servers:
        print("MCP_PROBE_FAILED: config or manifest has no servers", file=sys.stderr)
        return 2

    failures: list[str] = []
    evidence: dict = {"epoch": int(time.time()), "config": args.config,
                      "servers": {}, "failures": failures}

    # 1. exact server set, both directions
    missing = sorted(set(man_servers) - set(cfg_servers))
    extra = sorted(set(cfg_servers) - set(man_servers))
    if missing:
        failures.append(f"config missing server(s): {','.join(missing)}")
    if extra:
        failures.append(f"config has EXTRA server(s) not in the manifest: "
                        f"{','.join(extra)}")

    # 4. denylist coverage — checked even if a server later fails, so the report
    # is complete in one pass
    deny = {d.strip() for d in os.environ.get("JCODE_TOOLS_DENY", "").split(",")
            if d.strip()}
    for base in man.get("base_denied") or []:
        if base not in deny:
            failures.append(f"denylist missing base tool '{base}'")
    for sname, sman in man_servers.items():
        for tool in sman.get("destructive") or []:
            full = f"mcp__{sname}__{tool}"
            if full not in deny:
                failures.append(f"denylist missing '{full}'")

    # 2+3+5. live probe per server (only servers present in BOTH sets)
    # A readcheck PER SERVER, not one for the whole surface. The single-server form
    # (`readcheck`) is still accepted and folded in, but it is what let Context7 pass
    # every boot for days while never being called once: listing tools proves a server
    # answered a handshake, not that a cycle can USE it. Context7's own troubleshooting
    # docs make the same point — verify with a real request, and check that an
    # unauthorized one is actually challenged, rather than assuming the wiring holds.
    readchecks = list(man.get("readchecks") or [])
    if man.get("readcheck"):
        readchecks.append(man["readcheck"])
    readcheck = man.get("readcheck") or {}
    for sname in sorted(set(man_servers) & set(cfg_servers)):
        spec = cfg_servers[sname]
        sev: dict = {"reachable": False}
        evidence["servers"][sname] = sev
        try:
            r = probe_server(sname, spec, args.timeout)
        except ServerError as e:
            failures.append(f"server '{sname}' unreachable: {e}")
            continue
        cli, tools = r["client"], r["tools"]
        try:
            sev.update({
                "reachable": True,
                "tool_count": len(tools),
                "tools_sha256": hashlib.sha256(
                    "\n".join(tools).encode()).hexdigest(),
            })
            live_destr = sorted(t for t in tools if DESTRUCTIVE_RE.search(t))
            want_destr = sorted(man_servers[sname].get("destructive") or [])
            sev["destructive_live"] = live_destr
            extra_d = sorted(set(live_destr) - set(want_destr))
            missing_d = sorted(set(want_destr) - set(live_destr))
            if extra_d:
                failures.append(
                    f"server '{sname}' exposes destructive tool(s) the manifest "
                    f"does not expect: {','.join(extra_d)} — review, deny, and "
                    f"add to the manifest before booting")
            if missing_d:
                failures.append(
                    f"server '{sname}' is MISSING expected destructive tool(s): "
                    f"{','.join(missing_d)} — stale manifest or wrong endpoint")
            for rc in [r for r in readchecks if r.get("server") == sname]:
                tool = rc.get("tool") or ""
                if tool not in tools:
                    failures.append(
                        f"readcheck tool '{tool}' not in '{sname}' tools/list")
                    continue
                res = cli.call_tool(tool, rc.get("arguments") or {})
                verdict = judge_readcheck(res)
                sev.setdefault("readchecks", []).append(
                    {"tool": tool, "ok": verdict == "", "detail": verdict or "ok"})
                sev["readcheck"] = sev["readchecks"][-1]   # back-compat for readers
                if verdict:
                    failures.append(
                        f"readcheck {sname}:{tool} failed: {verdict}")
        except ServerError as e:
            failures.append(f"server '{sname}' failed mid-probe: {e}")
        finally:
            cli.close()

    # The read call is REQUIRED, not best-effort: a manifest without one, or a
    # pass where it silently never ran, is not a proven boot (gate B9).
    if not readchecks:
        failures.append("manifest defines no readcheck — a boot without one "
                        "proven read-only call is not a proven boot")
    # Every server named in the manifest's `servers` block must have a readcheck, and
    # every readcheck must have actually run. Silence is not a pass: the failure this
    # guards against is a server that lists tools and then errors on every call.
    for sname in sorted(man_servers):
        if any(r.get("server") == sname for r in readchecks):
            continue
        # An exemption must be WRITTEN DOWN with a reason. A server can be genuinely
        # unreadable without side effects (browseros drives a real browser), but that
        # has to be a visible decision in the manifest, not an omission nobody notices.
        why = (man_servers[sname] or {}).get("readcheck_exempt")
        if not why:
            failures.append(
                f"no readcheck defined for '{sname}' — tools/list alone does not "
                f"prove a cycle can call it. Add one, or set readcheck_exempt with "
                f"a reason.")
    for rc in readchecks:
        rcs = rc.get("server") or ""
        if not rcs or not rc.get("tool"):
            failures.append(f"malformed readcheck entry: {rc!r}")
            continue
        ran = [x for x in evidence["servers"].get(rcs, {}).get("readchecks", [])
               if x.get("tool") == rc.get("tool")]
        if not ran and not any(rcs in f for f in failures):
            failures.append(f"readcheck on '{rcs}' never executed")

    if args.evidence:
        try:
            tmp = args.evidence + f".tmp.{os.getpid()}"
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(evidence, fh, indent=1)
            os.replace(tmp, args.evidence)
        except OSError as e:
            # evidence is part of the audit trail; failing to write it is a
            # probe failure, not a shrug
            failures.append(f"cannot write evidence file: {e}")

    if failures:
        for f in failures:
            print(f"MCP_PROBE_MISSING: {f}", file=sys.stderr)
        return 1

    served = ",".join(sorted(evidence["servers"]))
    rc = evidence["servers"].get(readcheck.get("server") or "", {}) \
        .get("readcheck", {})
    # Report EVERY readcheck, not just one. The boot line is the only place an operator
    # sees this, and a summary that names a single server is how "Context7 is wired" went
    # unchallenged while it was never called.
    shown = []
    for r in readchecks:
        got = [x for x in evidence["servers"].get(r.get("server") or "", {})
               .get("readchecks", []) if x.get("tool") == r.get("tool")]
        shown.append("%s:%s:%s" % (r.get("server"), r.get("tool"),
                                   "ok" if got and got[0].get("ok") else "MISSING"))
    exempt = sorted(k for k, v in man_servers.items() if (v or {}).get("readcheck_exempt"))
    print(f"MCP_PROBE_OK servers={served} "
          f"readchecks={','.join(shown) or 'NONE'} "
          + (f"exempt={','.join(exempt)} " if exempt else "")
          + f"denylist_entries={len(deny)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
