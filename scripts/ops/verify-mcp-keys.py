#!/usr/bin/env python3
"""After a deploy: does each MCP server actually receive a well-formed key?

Run inside the container, ideally right after a swap and before the hold is released.

  verify-mcp-keys.py                      # PASS/FAIL per server, no secret ever printed

## Why it reads /proc and not its own environment

The first version of this script ran each `.mcp.json` command's key-resolution prefix in a
fresh shell and reported the result. It called Airtable and Linear BROKEN in production when
both were fine. `docker exec` starts a shell that has NOT sourced the entrypoint, so
`runtime.env`-supplied keys are simply absent from it — while the loop, which did source it,
has them. Context7 looked healthy in the same run only because its key comes from a lower
config layer that every shell inherits.

That is the documented gotcha in this codebase ("`docker exec … echo $VAR` shows a FRESH
shell's env, not the entrypoint-sourced env the loop has"), and measuring the wrong
environment produces a confident, wrong answer. So this reads the LOOP PROCESS's own
environment — lengths and shape only, never a value — because that is the environment the
MCP children are actually spawned from.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys

CONFIG = "/app/.mcp.json"
# server -> (env var, the shape a real key has, human name for the shape)
EXPECT = {
    "airtable": ("AIRTABLE_API_KEY", lambda v: "." in v, "contains a dot"),
    "linear": ("LINEAR_API_KEY", lambda v: v.startswith("lin_api_"), "starts with lin_api_"),
    "context7": ("CONTEXT7_API_KEY", lambda v: v.startswith("ctx7sk"), "starts with ctx7sk"),
}


def loop_env() -> dict[str, str]:
    """The loop's own environment. Values stay in this process and are never printed."""
    pid = subprocess.run(["pgrep", "-f", "auto-loop.sh"], capture_output=True, text=True).stdout.split()
    if not pid:
        raise SystemExit("no auto-loop.sh process — run this in the container, with the loop up")
    with open("/proc/%s/environ" % pid[0], "rb") as fh:
        raw = fh.read().decode("utf-8", "replace")
    out = {}
    for item in raw.split("\0"):
        k, _, v = item.partition("=")
        if k:
            out[k] = v
    return out


def main() -> int:
    env = loop_env()
    cfg = json.load(open(CONFIG))["mcpServers"]
    bad = 0
    for name, (var, shape_ok, shape) in EXPECT.items():
        srv = cfg.get(name, {})
        val = env.get(var, "")
        wrapped = srv.get("command") == "sh" and "security find-generic-password" in \
            (srv.get("args") or ["", ""])[1]
        if not val:
            # No key in the loop's env means the fallback decides — and on Linux there is no
            # `security` binary, so the fallback cannot save it either.
            print("%-10s FAIL  absent from the loop's environment" % name)
            bad += 1
            continue
        ok = shape_ok(val)
        print("%-10s %s  len=%d, %s, wrapper=%s" % (
            name, "PASS " if ok else "FAIL ", len(val), shape if ok else "WRONG SHAPE",
            "yes" if wrapped else "NO"))
        bad += not ok
    print("%d server(s) failing" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
