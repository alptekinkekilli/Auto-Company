#!/usr/bin/env python3
"""Resume lint'i — "yabancı-okur testi"nin MEKANİK yarısı.

NEDEN: ritüelin son adımı (yabancı-okur testi) tamamen vicdana kalıyordu; canlı
kullanımda resume'a yazılmış bayat bir SAYI yanlış temelde karar aldırdı ve bir
başka gün iki compact üst üste ritüeli yarıda kesti. Bu betik iki şeyi compact
ÖNCESİ, exit code ile yakalar:
  1. "metin karar taşır, sayı taşımaz" ihlalleri (maliyet/kuyruk/süreç/doluluk
     sayıları resume'a yazılmaz — session-brief compact sonrası yeniden ölçer);
  2. şablon bölümlerinin eksikliği (şablon: .claude/skills/compact-ritual/
     resume-template.md — özellikle DOĞRULANMAMIŞ ayrımı ve BEKLEYEN KARAR).

Commit SHA'ları ve iş/görev id'leri SERBESTTİR: onlar çapa/referanstır,
bayatlayan ölçüm değildir.

Kullanım: python3 scripts/compact-resume-lint.py [/tmp/compact-resume.md]
Çıkış: 0 temiz; 1 ihlal (satır numarası + gerekçeyle listeler).
"""
from __future__ import annotations

import re
import sys

VARSAYILAN = "/tmp/compact-resume.md"

# Her desen gerçek bir kazadan türedi; yenisini eklerken gerekçesini yaz.
YASAK = (
    (r"\$\s*\d", "para tutarı — maliyet/bütçe brifing yeniden ölçer"),
    (r"\bpending=\d", "kuyruk sayısı — brifing yeniden ölçer"),
    (r"\bin-progress=\d", "kuyruk sayısı — brifing yeniden ölçer"),
    (r"(harcan|tavan|bütçe)\w*\W{0,4}\d", "bütçe iddiası — brifing yeniden ölçer"),
    (r"(bağlam|doluluk)\W{0,6}%\s*\d", "doluluk yüzdesi — context-watch ölçer"),
)

# Şablondaki bölümler; alt-küme araması (başlık biçimi esnek kalabilsin diye).
ZORUNLU = ("İLK İŞ", "KARAR", "DOĞRULANMAMIŞ", "BEKLEYEN", "İZLEYİCİ")


def main() -> int:
    yol = sys.argv[1] if len(sys.argv) > 1 else VARSAYILAN
    try:
        satirlar = open(yol, encoding="utf-8").read().splitlines()
    except Exception as e:
        print(f"LINT KIRMIZI: {yol} okunamadı ({e}) — ritüelin resume adımı çalışmamış.")
        return 1

    hatalar: list[str] = []
    if len([s for s in satirlar if s.strip()]) < 10:
        hatalar.append("dosya taslak/boş görünüyor (<10 dolu satır) — şablonu doldur")
    govde = "\n".join(satirlar)
    if "<tarih>" in govde or "<karar metni birebir>" in govde:
        hatalar.append("şablon yer-tutucuları duruyor — gerçek içerikle değiştir")
    for ad in ZORUNLU:
        if ad not in govde:
            hatalar.append(f"zorunlu bölüm yok: '{ad}' (şablon: resume-template.md)")
    for i, s in enumerate(satirlar, 1):
        if s.lstrip().startswith("<!--"):
            continue
        for desen, neden in YASAK:
            if re.search(desen, s, re.IGNORECASE):
                hatalar.append(f"satır {i}: {neden} | {s.strip()[:90]}")

    if hatalar:
        print(f"LINT KIRMIZI ({yol}):")
        for h in hatalar:
            print(f"  ✗ {h}")
        print("Düzeltme yolu: sayıyı SİL ya da ölçüm KOMUTUNA çevir "
              "('şu an X' değil 'X'i şununla ölç'); eksik bölümü şablondan ekle.")
        return 1
    print(f"LINT YEŞİL: {yol} — sayı taşımıyor, zorunlu bölümler tam.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
