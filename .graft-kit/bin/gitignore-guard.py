#!/usr/bin/env python3
"""graft'ın .gitignore'a geri eklediği 'graft/' (veya 0.13+ formatında '/graft/') satırını kaldırır.

NEDEN: Kartları versiyonlama kararı (bkz. CLAUDE.md > "Graft kart kuralı") graft'ın
kendi yazma davranışıyla çakışıyor. `graft build` VE graft'ın Claude Code hook'ları
her koşuda .gitignore'a "graft/" satırını geri ekliyor; git dışlanmış bir dizinin
içeriğini negation ile geri dâhil edemediği için yeni kartlar sessizce ignore'a düşüyor.

Sarmalayıcı (graft-build.sh) bunu zaten çağırıyor; hook olarak da bağlı ki sarmalayıcıyı
atlayan graft koşuları da temizlensin.

Çıktı: yalnızca değişiklik yaptıysa tek satır yazar (sessiz-varsayılan).
"""
import re
import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    p = root / ".gitignore"
    if not p.is_file():
        return 0
    s = orig = p.read_text(encoding="utf-8")
    # graft 0.10 yazar "graft/", 0.13+ yazar "/graft/" (leading slash) — ikisini de yakala.
    if not re.search(r"(?m)^/?graft/$", s):
        return 0
    # graft'ın eklediği bloğu (yorum satırı varsa onunla birlikte) kaldır
    s = re.sub(r"\n*# graft's local graph cache[^\n]*\n/?graft/\n", "\n", s)
    s = re.sub(r"(?m)^/?graft/\n", "", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    if s != orig:
        p.write_text(s, encoding="utf-8")
        print("  .gitignore: graft'ın eklediği 'graft/' satırı kaldırıldı (kartlar versiyonlanıyor)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
