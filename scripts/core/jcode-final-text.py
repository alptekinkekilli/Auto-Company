#!/usr/bin/env python3
"""Extract the full assistant text from a jcode --ndjson stream — the ONE implementation.

Why this is not a one-line jq: **`done.text` is not reliably the whole answer.**
Measured 2026-07-31 on a tool-using run: the model's final message was

    **Title:** auto-loop: 1500s timeout kill leaves claude child alive …
    **State:** Backlog

every character of it arriving in 31 `text_delta` events after the tool call — and yet
`done.text` carried only `**State:** Backlog`, the last block. On a run with no tool call
and a single short block, `done.text` IS the whole answer, which is exactly why this hid:
the analyst's 42k-char reports came through `done.text` intact and nothing looked wrong.

A truncation like that is silent. A cycle SUMMARY would lose everything except its last
paragraph, and the loop would log a healthy-looking line. So: take BOTH readings and keep
the longer one. Concatenated deltas can additionally include narration emitted before a
tool call, which is noise but never loss; `done.text` can be a fragment, which is loss.
Prefer noise.

Usage:  jcode-final-text.py <events.ndjson>   # prints the text, exit 1 if empty
"""

from __future__ import annotations

import json
import sys


def final_text(path: str) -> str:
    deltas: list[str] = []
    done_text = ""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            t = ev.get("type")
            if t == "text_delta":
                deltas.append(str(ev.get("text") or ""))
            elif t == "done":
                done_text = str(ev.get("message") or ev.get("text") or "")
    joined = "".join(deltas)
    return joined if len(joined) > len(done_text) else done_text


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: jcode-final-text.py <events.ndjson>", file=sys.stderr)
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
