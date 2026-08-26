#!/usr/bin/env python3
"""compact ritüeli: çekirdek ANKOR string'leri dört köşede senkron KALMALI.

NEDEN: ritüelin çekirdek ankorları ("İLK İŞ", "KARAR", "DOĞRULANMAMIŞ",
"BEKLEYEN", "İZLEYİCİ") DÖRT ayrı yerde tekrarlanır ama aralarında mekanik bir
eşitlik kapısı yoktur:

  1. scripts/compact-resume-lint.py  → ZORUNLU  (resume'da bu bölümler VAR MI)
  2. scripts/compact-postcheck.py    → ANKORLAR (compact_summary bunları TAŞIDI MI)
  3. .claude/skills/compact-ritual/resume-template.md → başlık metinleri
  4. tests/test_compact_ritual_hardening.sh → lint-geçen/summary fixture'larındaki sabit liste

Kod yorumları "senkron tutulmalı" der ama bu bir DİLEK'tir, kapı değil. Biri
6. ankor ekleyip diğerlerini unutursa: lint yanlış bölüm setini zorunlu tutar,
postcheck kanaryası özet içinde YANLIŞ ankorları arar (sahte kayıp/sahte taşındı),
hardening testinin fixture'ı bayatlar. Üçü de "unutkanlık" sınıfı — tam da ritüel
sertleştirmesinin hedefi. Bu betik o drift'i test-zamanı exit code ile yakalar.

SÖZLEŞME:
  - ANKORLAR (postcheck) ile ZORUNLU (resume-lint) BİREBİR eşit (öğe + sıra).
  - Her ankor, doldurulmuş resume'un lint'i geçebilmesi için şablonda alt-string
    olarak geçer.
  - Her ankor, davranış testinin (hardening .sh) fixture'ında geçer.
  - Liste sabit uzunlukta değil: sayı hardcode edilmez; kural eşitlik + kapsanma,
    böylece ankor eklemek/çıkarmak tek kaynakta yapılıp burada doğrulanır.

Kullanım:
  pytest tests/test_compact_anchor_sync.py -q
  python3 tests/test_compact_anchor_sync.py
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FAILURES: list[str] = []


def _load(mod_name: str, rel: str):
    spec = importlib.util.spec_from_file_location(mod_name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(name, actual, expected):
    if actual == expected:
        print(f"ok   {name}")
    else:
        print(f"FAIL {name}: {actual!r} != {expected!r}")
        FAILURES.append(name)


postcheck = _load("cpc", "scripts/compact-postcheck.py")
resume_lint = _load("crl", "scripts/compact-resume-lint.py")

ANKORLAR = getattr(postcheck, "ANKORLAR", None)
ZORUNLU = getattr(resume_lint, "ZORUNLU", None)

check("postcheck ANKORLAR tanımlı ve boş değil", bool(ANKORLAR), True)
check("resume-lint ZORUNLU tanımlı ve boş değil", bool(ZORUNLU), True)
check("ANKORLAR == ZORUNLU (birebir)", ANKORLAR, ZORUNLU)

tmpl = (ROOT / ".claude/skills/compact-ritual/resume-template.md").read_text(encoding="utf-8")
for a in (ANKORLAR or ()):
    check(f"şablon '{a}' ankorunu içeriyor", a in tmpl, True)

# 4. köşe: davranış testinin fixture'ı — yalnız o test dosyası varsa denetlenir
# (kit'in ileride hardening.sh'sız kurulumu bu testi kırmasın).
hardening = ROOT / "tests/test_compact_ritual_hardening.sh"
if hardening.is_file():
    metin = hardening.read_text(encoding="utf-8")
    for a in (ANKORLAR or ()):
        check(f"hardening fixture'ı '{a}' içeriyor", a in metin, True)
else:
    print("ok   (tests/test_compact_ritual_hardening.sh yok — 4. köşe atlandı)")

# ÇAPA: bugünkü ankor seti. Tuple'ı dışarıdan sabitlemek değil — kasıtlı bir
# değişiklikte bu satır da güncellenir ve diff, "tüm ankorlar bilerek mi değişti"
# sorusunu reviewer'a açıkça sorar (sessiz tek-taraflı düzenlemeyi engeller).
BEKLENEN = ("İLK İŞ", "KARAR", "DOĞRULANMAMIŞ", "BEKLEYEN", "İZLEYİCİ")
check("ankor seti bilinen çapayla uyumlu (kasıtlı değişimde bu satır da güncellenir)",
      tuple(ANKORLAR or ()), BEKLENEN)


def test_hepsi_gecti():
    assert not FAILURES, "%d basarisiz: %s" % (len(FAILURES), FAILURES)


if __name__ == "__main__":
    if FAILURES:
        print(f"\n{len(FAILURES)} FAILED")
        sys.exit(1)
    print("\nTÜMÜ GEÇTİ")
