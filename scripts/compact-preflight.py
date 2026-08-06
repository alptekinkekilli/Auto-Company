#!/usr/bin/env python3
"""Compact ön-kontrolü — PreCompact hook'undan (manual VE auto) otomatik koşar.

NEDEN: compact ritüeli "operatör haber verir + ajan hatırlar" varsayımına dayanır.
İki delik: otomatik compact haber vermez, hatırlama garanti değildir. Bu betik
ritüelin ÖLÇÜLEBİLİR kısmını koda çevirir — kaybolursa acıtacak şeyleri sayar.

Çıktı iki yere gider: stdout (hook günlüğü) ve /tmp/compact-preflight.md — compact
SONRASI session-brief bunu okuyup açık kalemleri yeni bağlama taşır.

Genişletme: PREFLIGHT_ROOTS env'i ile ek git kökleri (iki nokta üst üste ayrılmış)
taranır. Projeye özel kontroller için .claude/preflight-extra.sh (çalıştırılabilir)
varsa koşulur ve çıktısı rapora eklenir — betiği fork'lamana gerek yok.
"""
from __future__ import annotations

import datetime as dt
import os
import subprocess

OUT = "/tmp/compact-preflight.md"


def sh(args, cwd=None):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def repo_report(root):
    if not os.path.isdir(os.path.join(root, ".git")) and not os.path.isfile(os.path.join(root, ".git")):
        return [], 0
    ad = os.path.basename(root.rstrip("/"))
    satir, risk = [f"- **{ad}**: `{sh(['git', 'log', '--oneline', '-1'], cwd=root) or '?'}`"], 0
    sb = sh(["git", "status", "-sb"], cwd=root).splitlines()
    basli = sb[0] if sb else ""
    if "[ahead" in basli:
        risk += 1
        satir.append(f"    - ⚠ PUSH EDİLMEMİŞ commit ({basli.split('[')[1].rstrip(']')})")
    dirty = [l for l in sb[1:] if l.strip() and not l.startswith("??")]
    if dirty:
        risk += 1
        satir.append(f"    - ⚠ KAYDEDİLMEMİŞ değişiklik: {len(dirty)} izlenen dosya")
    if sh(["git", "stash", "list"], cwd=root):
        risk += 1
        satir.append("    - ⚠ STASH'te iş var (yarım kalmış olabilir)")
    return satir, risk


def main() -> int:
    roots = [os.getcwd()] + [r for r in os.environ.get("PREFLIGHT_ROOTS", "").split(":") if r]
    L = [f"# Compact ön-kontrolü — {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    risk = 0
    for r in roots:
        s, x = repo_report(r)
        L += s
        risk += x

    ek = os.path.join(os.getcwd(), ".claude", "preflight-extra.sh")
    if os.access(ek, os.X_OK):
        cikti = sh(["bash", ek])
        if cikti:
            L += ["", "## Projeye özel kontroller", cikti]
            risk += cikti.count("⚠")

    L += ["", "## Compact sonrası ilk iş", "",
          "1. `python3 scripts/session-brief.py` çıktısını oku — SAYILAR oradan gelir, özetten değil.",
          "2. Arka plan izleyicileri öldüyse yeniden kur; kurmadan ÖNCE süreç kontrolü yap (mükerrer kurma).",
          "3. Aşağıdaki ⚠ satırlarının her birini doğrula; hâlâ açık olan varsa önce onu kapat."]
    L.insert(1, (f"**{risk} açık kalem — compact bunları özete taşımayabilir.**\n"
                 if risk else "**Açık kalem yok; compact güvenli.**\n"))

    metin = "\n".join(L)
    try:
        open(OUT, "w").write(metin)
    except Exception:
        pass
    print(metin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
