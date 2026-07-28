"""Lint: `[ test ] && action` in a position where a false test kills the script.

Under `set -e`, that construct returns 1 when the test is false. That is harmless
mid-function, but fatal in two positions:

  * as a function's LAST command   -> the function returns 1, killing an unguarded caller
  * immediately before a bare `return` -> the bare return inherits the 1, same result

Both shapes were live in scripts/core/auto-loop.sh and one of them (a different
function) took the container down every ~5 minutes for three days (APP-240). This
lint exists so the shape cannot come back unnoticed.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    ROOT / "scripts" / "core" / "auto-loop.sh",
    ROOT / "docker-entrypoint.sh",
]

# Scope note, measured in bash 2026-07-28 — do NOT widen this lint to every block
# terminator. `set -e` exempts the LEFT operand of an AND-OR list, so `[ x ] && y`
# is survivable as the last statement before `done`, `fi`, or `esac`. It is fatal
# only where the list's exit status becomes the status of something `set -e` checks:
#   * the last statement of a FUNCTION body   -> the caller sees rc=1   (checked here)
#   * immediately before a bare `return`      -> the return inherits it (checked here)
#   * the last statement of a loop fed by a PIPE (`cmd | while ...; done`), because
#     the pipeline inherits the loop's status — but a loop fed by a REDIRECT
#     (`done < file`) does NOT, and the two are indistinguishable to a line-based
#     scan. Flagging `done` outright would fire on the safe redirect form, which is
#     what docker-entrypoint.sh's runtime.env parser uses.
FUNC_START = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\(\)\s*\{")
TEST_AND = re.compile(r"^\[\s.*\s\]\s*&&\s")
# `... || true` / `... || :` makes the whole list return 0, so the shape is safe.
SAFE_TAIL = re.compile(r"\|\|\s*(true|:)\s*$")


def _is_fatal_shape(line: str) -> bool:
    return bool(TEST_AND.match(line)) and not SAFE_TAIL.search(line)


def _executable_lines(lines: list[str], offset: int = 1) -> list[tuple[int, str]]:
    out = []
    for i, raw in enumerate(lines, offset):
        s = raw.strip()
        if s and not s.startswith("#"):
            out.append((i, s))
    return out


def find_violations(path: Path) -> list[str]:
    lines = path.read_text().splitlines()
    bad: list[str] = []
    func = None
    start = 0
    for i, raw in enumerate(lines, 1):
        m = FUNC_START.match(raw)
        if m:
            func, start = m.group(1), i
            continue
        if raw == "}" and func:
            body = _executable_lines(lines[start : i - 1], offset=start + 1)
            if body:
                lineno, last = body[-1]
                if _is_fatal_shape(last):
                    bad.append(
                        f"{path.name}:{lineno} {func}() ends with a `[ ] &&` list "
                        f"-> returns 1 when the test is false: {last}"
                    )
            func = None

    # `[ ] && ...` immediately followed by a bare `return`
    body = _executable_lines(lines)
    for (ln, cur), (_, nxt) in zip(body, body[1:]):
        if _is_fatal_shape(cur) and nxt == "return":
            bad.append(
                f"{path.name}:{ln} `[ ] &&` list immediately before a bare `return` "
                f"-> the return inherits its exit status: {cur}"
            )
    return bad


class SetEShapeLint(unittest.TestCase):
    def test_no_fatal_test_and_shapes(self) -> None:
        violations: list[str] = []
        for p in SCRIPTS:
            if p.is_file():
                violations.extend(find_violations(p))
        self.assertEqual(
            violations,
            [],
            "\n\nUnder `set -e` these return 1 when the test is false and kill the "
            "caller. Use an explicit `if` block and an explicit `return 0`:\n  - "
            + "\n  - ".join(violations),
        )


if __name__ == "__main__":
    unittest.main()
