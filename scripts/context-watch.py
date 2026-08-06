#!/usr/bin/env python3
"""Bağlam doluluk gözcüsü — operatör kuralı 2026-08-05: %50'de UYAR, %60'ta RİTÜELİ UYGULA.

Neden hook: doluluk oranını oturum içinden güvenilir biçimde göremiyorum; transcript
dosyasındaki son asistan mesajının usage alanı bunu VERİR. Bağlam boyutu =
input + cache_read + cache_creation (o istekte modele giden toplam).

Nerede koşar: UserPromptSubmit ve PostToolUse (ikisi de transcript_path taşır ve
hookSpecificOutput.additionalContext ile bağlama yazabilir — additionalContext'i
hookSpecificOutput İÇİNE koymak zorunlu, dışarıda sessizce yok sayılır).

Gürültü kontrolü: her eşik oturum başına BİR kez tetiklenir (/tmp/context-watch-<sid>.json).
Compact sonrası doluluk düşerse durum sıfırlanır, eşikler yeniden silahlanır —
compact'tan sonra ikinci bir dolma da yakalanır.

Ayarlar (env): CONTEXT_WINDOW (varsayılan 200000), CONTEXT_WARN (50), CONTEXT_ACT (60).
"""
from __future__ import annotations

import json
import os
import sys

# Pencere SABİT VARSAYILMAZ (2026-08-05, ilk canlı atış "%257" dedi): oturumun modeli
# 200k'dan büyük bir pencerede koşuyordu. Ölçülen bağlam varsayılan pencereyi aşarsa
# bilinen kademelere yükseltilir — yüzde anlamsızlaşacağına kendini düzeltir.
KADEMELER = (200_000, 500_000, 1_000_000, 2_000_000)
WINDOW = int(os.environ.get("CONTEXT_WINDOW", "200000"))
WARN = int(os.environ.get("CONTEXT_WARN", "50"))
ACT = int(os.environ.get("CONTEXT_ACT", "60"))


def kullanim(transcript: str) -> int | None:
    """Son asistan mesajının usage'ından ANLIK bağlam boyutu."""
    try:
        with open(transcript, "rb") as fh:
            satirlar = fh.readlines()[-400:]  # son mesajlar yeter; dosya çok büyük olabilir
    except Exception:
        return None
    for ham in reversed(satirlar):
        try:
            r = json.loads(ham)
        except Exception:
            continue
        u = ((r.get("message") or {}).get("usage")) or r.get("usage")
        if isinstance(u, dict) and u.get("input_tokens") is not None:
            return (int(u.get("input_tokens") or 0)
                    + int(u.get("cache_read_input_tokens") or 0)
                    + int(u.get("cache_creation_input_tokens") or 0))
    return None


def main() -> int:
    try:
        olay = json.load(sys.stdin)
    except Exception:
        return 0  # fail-open: gözcü asla akışı bozmaz
    tokens = kullanim(olay.get("transcript_path") or "")
    if not tokens:
        return 0
    pencere = WINDOW
    if tokens > pencere:
        pencere = next((k for k in KADEMELER if k > tokens), KADEMELER[-1])
    yuzde = round(100 * tokens / pencere)
    sid = olay.get("session_id", "yok")
    durum_yolu = f"/tmp/context-watch-{sid}.json"
    try:
        durum = json.load(open(durum_yolu))
    except Exception:
        durum = {"warn": False, "act": False}
    # Compact sonrası düşüş: eşikleri yeniden silahlandır. Sıfırlama DİSKE de yazılır —
    # aksi halde mesaj üretilmediği için kaybolur ve ikinci dolma sessiz geçer (test yakaladı).
    if yuzde < WARN - 10 and (durum.get("warn") or durum.get("act")):
        durum = {"warn": False, "act": False}
        try:
            json.dump(durum, open(durum_yolu, "w"))
        except Exception:
            pass

    mesaj = None
    if yuzde >= ACT and not durum["act"]:
        durum["act"] = durum["warn"] = True
        mesaj = (f"[BAĞLAM %{yuzde}] Operatör kuralı: %{ACT} eşiği aşıldı — COMPACT RİTÜELİNİ ŞİMDİ UYGULA. "
                 f"Adımlar `.claude/skills/compact-ritual/SKILL.md` dosyasında: `python3 scripts/compact-preflight.py` "
                 f"koş, ⚠ açık kalemlerin her birini kapat ya da resume'a 'İLK İŞ' olarak yaz, sonra KARAR taşıyan "
                 f"(sayı taşımayan) resume bloğunu tek mesajda operatöre ver ve compact'i onun başlatacağını söyle. "
                 f"Uçuşta zincir varsa önce onu bitir/park et.")
    elif yuzde >= WARN and not durum["warn"]:
        durum["warn"] = True
        mesaj = (f"[BAĞLAM %{yuzde}] Uyarı eşiği (%{WARN}). Henüz ritüel gerekmiyor; %{ACT}'ta otomatik tetiklenecek. "
                 f"Şimdiden: uzun tool çıktılarını kırp, bitmiş işleri kapat, operatöre doluluğu bir cümleyle bildir.")

    if not mesaj:
        return 0
    try:
        json.dump(durum, open(durum_yolu, "w"))
    except Exception:
        pass
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": olay.get("hook_event_name", "PostToolUse"),
        "additionalContext": mesaj}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
