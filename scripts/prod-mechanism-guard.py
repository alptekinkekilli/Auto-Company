#!/usr/bin/env python3
"""Prod-mekanizma tripwire — PreToolUse hook'u (Edit|Write|NotebookEdit).

NEDEN: CLAUDE.md'nin "Prod-Mechanism Change Rule" bölümü plan+onay ister ama
düzyazı kural atlanabilir (enforceable-guardrails: okunan kural ≠ uygulatan
mekanizma). Bu betik korunan yüzeylere plansız yazma girişimini MEKANİK bloklar.

Tripwire'dır, boundary değil (directive-slot T4 felsefesiyle aynı): amaç kötü
niyeti durdurmak değil, "plansız dalma"yı yakalamak. Operatör onayı SONRASI
oluşturulan marker (.claude/.prod-change-approved, 120 dk geçerli) yazmayı açar.

Container'da (CLAUDE_PROJECT_DIR=/app) no-op — otonom cycle'lar PROMPT.md'nin
OPREQ/authorization makinesine tabidir; bu kural interactive oturumlar içindir.
Bozuk stdin fail-open (girdiyi harness'ın kendisi üretir; format değişimi tüm
edit'leri kilitlememeli) ama stderr'e uyarı basar. Bilinen sınır: Bash `sed -i`
bu guard'ı görmez — kapsam normal Edit/Write yolu.
"""
from __future__ import annotations

import json
import os
import sys
import time

MARKER_TTL_SECONDS = 120 * 60
GUARDED_TOOLS = {"Edit", "Write", "NotebookEdit"}
# CLAUDE.md "Prod-Mechanism Change Rule" listesiyle birebir tutulur.
PROTECTED_SUFFIXES = (
    "scripts/core/auto-loop.sh",
    "scripts/core/directive_writer.py",
    "scripts/ops/send-gate.py",
    "dashboard/server.py",
    "docker-entrypoint.sh",
)
PROTECTED_BASENAMES = {"Dockerfile", "runtime.env"}


def main() -> int:
    proj = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if proj == "/app" or proj.startswith("/app/"):
        return 0

    try:
        payload = json.load(sys.stdin)
    except Exception:
        print("[prod-guard] stdin JSON çözülemedi — fail-open, denetimsiz geçiş", file=sys.stderr)
        return 0

    if payload.get("tool_name") not in GUARDED_TOOLS:
        return 0
    ti = payload.get("tool_input") or {}
    fp = ti.get("file_path") or ti.get("notebook_path") or ""
    if not fp:
        return 0

    norm = os.path.abspath(fp)
    protected = any(norm.endswith(s) for s in PROTECTED_SUFFIXES) or (
        os.path.basename(norm) in PROTECTED_BASENAMES
    )
    if not protected:
        return 0

    marker = os.path.join(proj or os.getcwd(), ".claude", ".prod-change-approved")
    stale = False
    try:
        age = time.time() - os.stat(marker).st_mtime
        if 0 <= age < MARKER_TTL_SECONDS:
            return 0
        stale = True
    except FileNotFoundError:
        pass

    rel = os.path.relpath(norm, proj) if proj else norm
    msg = (
        f"[prod-guard] KORUNAN YÜZEY: {rel}\n"
        "CLAUDE.md 'Prod-Mechanism Change Rule': önce Plan Mode (EnterPlanMode) ile plan+etki\n"
        "sun, operatör onayını bekle. Onay ALINDIYSA marker oluştur (120 dk geçerli):\n"
        "  touch .claude/.prod-change-approved\n"
    )
    if stale:
        msg += "(Mevcut marker BAYAT — onay 120 dk'yı aştı; operatörden yeniden onay iste.)\n"
    print(msg, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
