#!/usr/bin/env python3
"""Compact operasyon digest'i — PreCompact hook'u.

NE: Her compact ritüelinde operatöre TEK operasyonel durum özeti basar. Compact
güvenlik ön-kontrolünü (`compact-preflight.py`) TEKRAR ETMEZ — onu tamamlar: preflight
"compact güvenli mi" der, bu script "şirket operasyonel olarak nerede" der.

NEDEN AYRI SCRIPT: preflight açık-kalem/güvenlik odaklı; session-brief compact SONRASI
(SessionStart) koşar. Operatör compact ANINDA (PreCompact) operasyonel bir fotoğraf
istedi (2026-08-27): repo↔prod sync, OPREQ, direktif, hold, bekleyen dış aksiyonlar,
son loop cycle/error/cost, loop canlılığı.

KURALLAR (session-brief ile aynı disiplin):
- İDDİA değil ÖLÇÜM basar; her satır o an ölçülür, bayatlayamaz.
- Fail-open: her ölçüm bağımsız try/except; hata → o satırı atla, ASLA sıfır-dışı çıkma,
  compact'i ASLA bloklama.
- Sır basmaz (token/ID yok); ssh yalnız BatchMode + timeout ile.
- Prod ölçümünün SUBTLE kısmını (image-vs-origin drift, direktif, opreq) yeniden
  yazmaz — tek doğruluk kaynağı `.claude/brief-extra.sh`'i çağırır (DRY).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import subprocess


def sh(args, cwd=None, timeout=12):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except Exception:
        return ""


def sh_input(args, stdin_text, timeout=15):
    try:
        return subprocess.run(args, input=stdin_text, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except Exception:
        return ""


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, ".."))


def line_repo(kok: str, L: list) -> None:
    try:
        head = sh(["git", "log", "--oneline", "-1"], cwd=kok) or "?"
        unpushed = sh(["git", "log", "--oneline", "origin/main..HEAD"], cwd=kok)
        n = len([x for x in unpushed.splitlines() if x.strip()]) if unpushed else 0
        tag = "push edilmemiş 0" if n == 0 else f"⚠ {n} commit PUSH EDİLMEMİŞ"
        L.append(f"- **repo**: `{head}` | {tag}")
    except Exception:
        pass


def block_prod(kok: str, L: list) -> None:
    """brief-extra.sh'i çağır: prod drift + hold + cockpit + direktif + opreq (DRY)."""
    try:
        be = os.path.join(kok, ".claude", "brief-extra.sh")
        if os.access(be, os.X_OK):
            out = sh(["bash", be], timeout=20)
            if out:
                L.append(out)
    except Exception:
        pass


def block_loop(L: list) -> None:
    """Tek ssh round-trip: cockpit State File (LOOP_COUNT/ERROR_COUNT/STATUS/ENGINE/
    MODEL) + son telemetri/cycle satırı + loop canlılığı + BOŞ-CYCLE serisi ve
    discretionary bütçe durumu (SUMMARY satırlarından — loop 'durmuş' görünüp aslında
    cost-guard'la boş dönerken bunu bir bakışta göster)."""
    try:
        remote = (
            'C=$(docker ps --format "{{.Names}}" | grep z12a992 | head -1); '
            '[ -z "$C" ] && { echo LOOP=no-container; exit 0; }; '
            'docker exec -u app "$C" sh -c '
            '\'curl -s -m5 http://127.0.0.1:8787/api/status 2>/dev/null; echo; '
            'cd /app 2>/dev/null && tail -n 120 logs/auto-loop.log 2>/dev/null | '
            'grep -E "\\[TELEMETRY\\]|Cycle #[0-9]+ \\[(OK|WAIT|START|ERR)" | tail -2; '
            'echo ===SUMMARY===; '
            'grep -hE "Cycle #[0-9]+ \\[SUMMARY\\]" logs/auto-loop.log 2>/dev/null | tail -20; '
            'echo ===END===; '
            'pgrep -f auto-loop.sh >/dev/null && echo LOOPPROC=alive || echo LOOPPROC=DEAD\''
        )
        out = sh(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8",
                  "powerupp-ts", remote], timeout=20)
        if not out:
            L.append("- **loop**: ULAŞILAMADI (ssh/prod?)")
            return
        if "LOOP=no-container" in out:
            L.append("- **loop**: konteyner yok")
            return
        # cockpit State File alanları JSON "raw" içinde düz metin
        def grab(key):
            m = re.search(rf"{key}=([^\s\\\"]+)", out)
            return m.group(1) if m else "?"
        lc, ec, st = grab("LOOP_COUNT"), grab("ERROR_COUNT"), grab("STATUS")
        eng, mdl = grab("ENGINE"), grab("MODEL")
        alive = "alive" if "LOOPPROC=alive" in out else ("DEAD" if "LOOPPROC=DEAD" in out else "?")
        # son cost: en son [TELEMETRY] cost=
        mcost = None
        for ln in out.splitlines():
            if "[TELEMETRY]" in ln:
                mm = re.search(r"cost=([0-9.]+)", ln)
                if mm:
                    mcost = mm.group(1)
        cost = f"${mcost}" if mcost else "?"
        warn = " ⚠" if (ec not in ("0", "?") or alive == "DEAD") else ""
        L.append(f"- **loop**: cycle #{lc} status={st} engine={eng}/{mdl} "
                 f"error={ec} son-cost={cost} proc={alive}{warn}")
        # son disposition satırı (kısa)
        for ln in reversed(out.splitlines()):
            m = re.search(r"(Cycle #\d+ \[(?:OK|WAIT|START|ERR)[^\n]*)", ln)
            if m:
                L.append(f"    - {m.group(1)[:120]}")
                break
        # BOŞ-CYCLE serisi (SUMMARY bölümünden; discretionary durumu ayrı — block_discretionary)
        try:
            body = out.split("===SUMMARY===", 1)[1].split("===END===", 1)[0]
            sums = [s for s in body.splitlines() if "[SUMMARY]" in s]
            empty_pat = re.compile(
                r"empty cycle|EMPTY|no permitted work|no work was permitted|"
                r"discretionary budget spent|recorded as an empty|no state changed",
                re.IGNORECASE)
            streak = 0
            for s in reversed(sums):          # sondan geriye ardışık boşları say
                if empty_pat.search(s):
                    streak += 1
                else:
                    break
            if streak > 0:
                L.append(f"    - ⚠ **iş durumu**: son {streak} cycle BOŞ (üretken iş yok)")
            else:
                L.append("    - **iş durumu**: üretken (son cycle boş değil)")
        except Exception:
            pass
    except Exception:
        pass


def block_discretionary(L: list) -> None:
    """Discretionary bütçe durumunu CANLI kaynaklardan oku (SUMMARY prose kazımaz):
    spend = bugünün discretionary-spend.ndjson toplamı, cap = ÇALIŞAN loop'un env'i
    (fiilen uygulanan değer), + runtime.env cap'i (bir sonraki boot'un değeri). İkisi
    farklıysa 'restart bekliyor' — runtime.env editlenmiş ama loop henüz source etmemiş."""
    py = (
        'import datetime,json,os,re\n'
        'd=datetime.datetime.now(datetime.timezone.utc).date().isoformat()\n'
        't=0.0\n'
        'try:\n'
        ' for x in open("/app/logs/discretionary-spend.ndjson"):\n'
        '  try:\n'
        '   r=json.loads(x)\n'
        '   if str(r.get("ts",r.get("date",""))).startswith(d): t+=float(r.get("cost",r.get("usd",0)) or 0)\n'
        '  except: pass\n'
        'except: pass\n'
        'capeff=""\n'
        'for p in [q for q in os.listdir("/proc") if q.isdigit()]:\n'
        ' try:\n'
        '  if "auto-loop.sh" in open("/proc/"+p+"/cmdline","rb").read().decode("utf-8","ignore"):\n'
        '   m=re.search(r"DISCRETIONARY_DAILY_CAP_USD=([0-9.]+)", open("/proc/"+p+"/environ","rb").read().decode("utf-8","ignore"))\n'
        '   if m: capeff=m.group(1); break\n'
        ' except: pass\n'
        'caprt=""\n'
        'try:\n'
        ' for x in open("/app/logs/runtime.env"):\n'
        '  m=re.match(r"DISCRETIONARY_DAILY_CAP_USD=([0-9.]+)", x.strip())\n'
        '  if m: caprt=m.group(1); break\n'
        'except: pass\n'
        'print("SPEND=%.2f"%t); print("CAPEFF="+capeff); print("CAPRT="+caprt)\n'
    )
    try:
        remote = ('C=$(docker ps --format "{{.Names}}" | grep z12a992 | head -1); '
                  '[ -z "$C" ] && exit 0; docker exec -i -u app "$C" python3 -')
        out = sh_input(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=8",
                        "powerupp-ts", remote], py, timeout=18)
        if not out:
            return
        def g(k):
            m = re.search(rf"{k}=([0-9.]*)", out)
            return m.group(1) if m and m.group(1) else None
        spend, capeff, caprt = g("SPEND"), g("CAPEFF"), g("CAPRT")
        if capeff is None:
            return
        over = "DOLU ⚠" if (spend and float(spend) >= float(capeff)) else "sınır altında"
        drift = ""
        if caprt and caprt != capeff:
            drift = f" ⚠ (runtime.env={caprt} — loop restart bekliyor)"
        sp = f"${spend}" if spend else "?"
        L.append(f"    - discretionary: {sp}/${capeff} {over}{drift}")
    except Exception:
        pass


def main() -> int:
    kok = repo_root()
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M")
    L = [f"## Compact operasyon digest'i — {ts} UTC",
         "Operasyonel durum (ölçüldü, iddia değil). Güvenlik ön-kontrolünü tamamlar; tekrar etmez."]
    line_repo(kok, L)
    block_prod(kok, L)
    block_loop(L)
    block_discretionary(L)
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        # fail-open: hiçbir koşulda compact'i bloklama
        raise SystemExit(0)
