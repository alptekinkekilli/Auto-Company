#!/usr/bin/env python3
"""Oturum brifingi — SessionStart hook'u (startup|resume|compact) stdout'unu doğrudan
bağlama enjekte eder.

NEDEN: elle yazılmış RESUME metinleri bayatlar ve içindeki SAYILAR yanlış karar
ürettirir. Brifing iddia taşımaz, o anda ÖLÇÜLEN durumu taşır — bayatlayamaz.

Kural: sır yazma, 2 sn'yi geçme, hata hâlinde satırı atla — brifing oturumu asla
bloklamaz. Projeye özel satırlar için .claude/brief-extra.sh (çalıştırılabilir)
varsa koşulur ve çıktısı eklenir.
"""
from __future__ import annotations

import datetime as dt
import os
import subprocess


def sh(args, cwd=None):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=8).stdout.strip()
    except Exception:
        return ""


def main() -> int:
    kok = os.getcwd()
    L = [f"## Oturum brifingi (ölçüldü {dt.datetime.now().strftime('%H:%M')})",
         "Aşağıdakiler İDDİA DEĞİL, şu anki ölçüm. Özet metniyle çelişirse ÖLÇÜM haklıdır."]

    dal = sh(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=kok) or "?"
    head = sh(["git", "log", "--oneline", "-1"], cwd=kok) or "?"
    sb = sh(["git", "status", "-sb"], cwd=kok).splitlines()
    senk = "eşit"
    if sb and ("[ahead" in sb[0] or "[behind" in sb[0]):
        senk = sb[0].split("[", 1)[1].rstrip("]")
    kirli = [l for l in sb[1:] if l.strip() and not l.startswith("??")]
    L.append(f"- **repo**: `{dal}` @ `{head}` | origin-{senk} | kirli izlenen dosya: {len(kirli)}")
    if kirli:
        L.append("    - " + " ".join(k.strip() for k in kirli[:8]) + (" …" if len(kirli) > 8 else ""))
    if sh(["git", "stash", "list"], cwd=kok):
        L.append("    - ⚠ stash'te iş var")

    ek = os.path.join(kok, ".claude", "brief-extra.sh")
    if os.access(ek, os.X_OK):
        cikti = sh(["bash", ek])
        if cikti:
            L.append(cikti)

    # PreCompact ön-kontrolü taze ise açık kalemleri yeni bağlama taşı.
    try:
        pf = "/tmp/compact-preflight.md"
        yas = (dt.datetime.now().timestamp() - os.path.getmtime(pf)) / 60
        if yas < 120:
            uyari = [s.strip() for s in open(pf).read().splitlines() if s.strip().startswith("- ⚠")]
            if uyari:
                L.append(f"- **Compact öncesi açık kalemler** ({int(yas)} dk önce): doğrula, körlemesine devralma")
                L += [f"    {u}" for u in uyari]
    except Exception:
        pass

    print("\n".join(L))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
