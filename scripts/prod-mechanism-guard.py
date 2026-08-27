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
import re
import sys
import time

MARKER_TTL_SECONDS = 120 * 60
GUARDED_TOOLS = {"Edit", "Write", "NotebookEdit"}
# CLAUDE.md "Prod-Mechanism Change Rule" listesiyle birebir tutulur.
PROTECTED_SUFFIXES = (
    "scripts/core/auto-loop.sh",
    "scripts/core/directive_writer.py",
    "scripts/ops/send-gate.py",
    "scripts/ops/rfq-send.py",
    "dashboard/server.py",
    "docker-entrypoint.sh",
)
PROTECTED_BASENAMES = {"Dockerfile", "runtime.env"}

# --check-sync: CLAUDE.md'nin kural bölümünde ANILAN ama bu betiğin korumadığı
# yüzey = kapsam kayması. Bölümde geçen ama yüzey olmayan backtick token'ları
# (uygulama mekanizmasının kendisi) burada dışlanır.
SYNC_IGNORE = {"scripts/prod-mechanism-guard.py", ".claude/.prod-change-approved"}
RULE_SECTION_RE = re.compile(
    r"^## Prod-Mechanism Change Rule.*?\n(.*?)(?=^## |\Z)", re.M | re.S
)
BACKTICK_TOKEN_RE = re.compile(r"`([^`\n]+)`")


def is_protected(path: str) -> bool:
    return any(path.endswith(s) for s in PROTECTED_SUFFIXES) or (
        os.path.basename(path) in PROTECTED_BASENAMES
    )


def check_sync(claude_md_path: str) -> int:
    """CLAUDE.md kural bölümü ↔ PROTECTED_* listesi senkron mu? Kayma = exit 1."""
    try:
        text = open(claude_md_path, encoding="utf-8").read()
    except OSError as exc:
        print(f"[prod-guard] check-sync: {claude_md_path} okunamadı: {exc}", file=sys.stderr)
        return 1
    m = RULE_SECTION_RE.search(text)
    if not m:
        print("[prod-guard] check-sync: 'Prod-Mechanism Change Rule' bölümü bulunamadı "
              "(bölüm silindi/yeniden adlandırıldıysa guard körleşti)", file=sys.stderr)
        return 1
    candidates = []
    for tok in BACKTICK_TOKEN_RE.findall(m.group(1)):
        tok = tok.strip()
        if "*" in tok or " " in tok or tok in SYNC_IGNORE:
            continue
        if tok.startswith("tests/"):
            continue  # test dosyaları hiçbir zaman korunan yüzey değildir
        if "/" in tok or tok in PROTECTED_BASENAMES or tok == "runtime.env":
            candidates.append(tok)
    uncovered = [c for c in candidates if not is_protected(c)]
    if uncovered:
        print("DRIFT: " + ", ".join(sorted(set(uncovered))))
        return 1
    print(f"OK: {len(set(candidates))} yüzey, hepsi kapsanıyor")
    return 0


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
    if not is_protected(norm):
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
    if len(sys.argv) > 1 and sys.argv[1] == "--check-sync":
        target = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
            os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()), "CLAUDE.md"
        )
        sys.exit(check_sync(target))
    sys.exit(main())
