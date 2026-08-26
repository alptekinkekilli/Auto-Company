#!/usr/bin/env python3
"""Extract the assistant's final message text from a `codex exec --json` event stream.

Why this exists (mirror of jcode-final-text.py, for the Codex CLI path): `codex exec
--json -o FILE` writes a JSONL EVENT STREAM to the -o file in the current CLI —
`thread.started` / `turn.started` / `item.completed{item:{type:"agent_message",text:…}}`
/ `turn.completed` — not the plain final message the older CLI wrote. `run_codex_cycle_cli`
used to `cat` that file straight into the cycle SUMMARY, so a Codex cycle's SUMMARY (and
thence Telegram, auto-loop.log, consensus, the state-snapshot baton) carried raw JSON like
`{"type":"thread.started",...}` instead of the model's answer.

The clean assistant answer is the text of the `item.completed` items whose
`item.type == "agent_message"`, in order. A turn may emit several (narration + final); we
concatenate them all — noise is never loss, the same principle jcode-final-text.py follows.
Non-agent_message items (reasoning, command_execution, mcp_tool_call) are ignored.

Fail-soft like its jcode sibling: skip malformed lines; print nothing (exit 1) if no
agent_message is found — the caller (auto-loop.sh) then falls back to the raw file content,
so an older plain-text `-o` or a schema change can never make the SUMMARY worse than before.

Usage:  codex-final-text.py <events.jsonl>   # prints the text, exit 1 if empty
"""

from __future__ import annotations

import json
import sys


def final_text(path: str) -> str:
    parts: list[str] = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("type") == "item.completed":
                item = ev.get("item") or {}
                if item.get("type") == "agent_message":
                    text = item.get("text")
                    if text:
                        parts.append(str(text))
    return "\n".join(parts)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: codex-final-text.py <events.jsonl>", file=sys.stderr)
        return 2
    try:
        text = final_text(sys.argv[1])
    except OSError as e:
        print(f"cannot read events: {e}", file=sys.stderr)
        return 2
    sys.stdout.write(text)
    return 0 if text.strip() else 1


if __name__ == "__main__":
    sys.exit(main())
