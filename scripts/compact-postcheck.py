#!/usr/bin/env python3
"""PostCompact denetim izi — compact BİTTİKTEN SONRA çalışır, hiçbir şeyi bloklayamaz.

NEDEN: ön-kontrol yalnız compact ÖNCESİ resume'un taze + lint-yeşil olduğunu
doğrular — ama hiçbir mekanizma, Claude Code'un kendi özetleyicisinin ÜRETTİĞİ
gerçek özetin (`compact_summary`) resume'un anahtar bölümlerini GERÇEKTEN taşıyıp
taşımadığını görmüyordu. Ritüel "resume'u yazdım" diyordu; "özetleyici onu fiilen
kullandı mı" hiç ölçülmüyordu — denetlenmeyen son halka.

Bu betik bloklayamaz (iş bittiğinde çalışır) ama dayanıklı bir İZ bırakır: bir şey
kaybolursa geriye dönük bakılabilir, ve kayıp-ankor listesi anlık bir UYARI olarak
da basılır. Kayıp tespiti bir KANIT değil bir KANARYADIR — özetleyici paraphrase
edebilir; yokluk her zaman kayıp demek değildir, ama varlığı ritüelin gerçekten
teslim edildiğine dair ölçülebilir bir sinyaldir.

Hook girdisi (stdin JSON): PostCompact `compact_summary` alanı taşır
(Claude Code hooks dokümanı). Env override'lar yalnız test içindir.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

RESUME = os.environ.get("COMPACT_RESUME_PATH", "/tmp/compact-resume.md")
LOG = os.environ.get("COMPACT_HISTORY_LOG", "/tmp/compact-history.log")

# compact-resume-lint.py'deki ZORUNLU tuple'la senkron tutulmalı — biri
# değişirse diğeri de gözden geçirilir.
ANKORLAR = ("İLK İŞ", "KARAR", "DOĞRULANMAMIŞ", "BEKLEYEN", "İZLEYİCİ")


def main() -> int:
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        payload = {}

    trigger = payload.get("trigger", "?")
    ozet = payload.get("compact_summary", "") or ""

    resume_var = False
    try:
        open(RESUME, encoding="utf-8").read()
        resume_var = True
    except Exception:
        pass

    tasinan = [a for a in ANKORLAR if a in ozet]
    kayip = [a for a in ANKORLAR if a not in ozet]

    satir = {
        "ts": dt.datetime.now().isoformat(timespec="seconds"),
        "trigger": trigger,
        "resume_var": resume_var,
        "ozet_uzunluk": len(ozet),
        "tasinan_ankorlar": tasinan,
        "kayip_ankorlar": kayip,
    }
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(satir, ensure_ascii=False) + "\n")
    except Exception:
        pass

    # compact_summary boşsa (bazı sürüm/tetik kombinasyonlarında olabilir) ya da
    # resume hiç yoksa kanarya anlamsızdır — sessiz kal, gürültü üretme.
    if ozet and resume_var and kayip:
        print(f"[compact-postcheck] kanarya: özet şu ankorları içermiyor görünüyor: {kayip} "
              f"— {LOG} dosyasına kaydedildi; bir şey kaybolduysa oradan geriye bak "
              f"(bu bir KANIT değil, paraphrase yanlış-pozitif üretebilir).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
