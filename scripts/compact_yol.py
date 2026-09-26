#!/usr/bin/env python3
"""Ritüel dosyalarının yolu — repo adına ÖZEL, tek kaynak.

NEDEN: kit ilk sürümlerde /tmp altında ORTAK sabit yollar kullanıyordu. Aynı
makinede iki proje compact'lenince biri ötekinin resume'unu "taze" sanıp okudu,
açık kalemler karıştı. Artık her yol repo adından türetilir:

    /tmp/compact-<ad>-resume.md      kanonik resume (ritüel adım 2)
    /tmp/compact-<ad>-preflight.md   PreCompact açık kalemleri
    /tmp/compact-<ad>-block.marker   otomatik compact erteleme işareti
    /tmp/compact-<ad>-history.log    PostCompact kanarya izi

<ad> nasıl bulunur (kök = BU dosyanın bir üst dizini; cwd DEĞİL — hook'lar
farklı cwd'den koşabilir):
  - `git rev-parse --git-common-dir`'in üst dizininin adı (worktree'de de ana
    repo adı). Son bileşen `.git` değilse (ör. submodule: `.git/modules/<x>`)
    `--show-toplevel`'ın adı.
  - Bağlı (linked) worktree'de, git-dir ≠ common-dir ise `-<worktree dizini adı>`
    eklenir: aynı reponun iki worktree'si de birbirinin resume'unu okumasın.
    Ana checkout'ta ek yoktur.
  - git yoksa / cevap vermezse: kök dizinin adı.
  - Ad [a-z0-9-]'e indirgenir; boş kalırsa `proje`.

Env override'ları her şeyden önce gelir (testler + özel kurulumlar):
COMPACT_RESUME_PATH, COMPACT_PREFLIGHT_PATH, COMPACT_BLOCK_MARKER,
COMPACT_HISTORY_LOG.

ESKİ ORTAK YOLLARA GERİ DÜŞÜŞ YOKTUR: onları okumak başka bir projenin durumunu
bu oturuma enjekte eder — düzeltilen hata tam olarak buydu.

Bu modül ASLA istisna fırlatmaz (hook'lar fail-open); git çağrıları zaman aşımlıdır.

Kullanım: python3 scripts/compact_yol.py [resume|preflight|marker|history|ad]
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[1]
GIT_ZAMAN_ASIMI_SN = 3
YEDEK_AD = "proje"
DESEN = "/tmp/compact-{ad}-{dosya}"

# tür → (env override, dosya soneki)
TURLER = {
    "resume": ("COMPACT_RESUME_PATH", "resume.md"),
    "preflight": ("COMPACT_PREFLIGHT_PATH", "preflight.md"),
    "marker": ("COMPACT_BLOCK_MARKER", "block.marker"),
    "history": ("COMPACT_HISTORY_LOG", "history.log"),
}


def temizle(ham: str) -> str:
    """Adı [a-z0-9-]'e indirger: küçük harf, diğer her şey '-', ardışık '-' tek."""
    ad = re.sub(r"[^a-z0-9]+", "-", (ham or "").lower()).strip("-")
    return ad or YEDEK_AD


def _git(kok: Path, *args: str) -> str:
    try:
        r = subprocess.run(["git", "-C", str(kok), *args], capture_output=True,
                           text=True, timeout=GIT_ZAMAN_ASIMI_SN)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def repo_adi(kok: str | os.PathLike | None = None) -> str:
    try:
        kok = Path(kok) if kok else KOK
        ortak = _git(kok, "rev-parse", "--path-format=absolute", "--git-common-dir")
        if not ortak:
            return temizle(kok.name)
        ust = _git(kok, "rev-parse", "--show-toplevel")
        ortak_p = Path(ortak)
        ad = ortak_p.parent.name if ortak_p.name == ".git" else Path(ust or kok).name
        gitdir = _git(kok, "rev-parse", "--path-format=absolute", "--git-dir")
        if gitdir and os.path.realpath(gitdir) != os.path.realpath(ortak):
            ad = f"{ad}-{Path(ust or kok).name}"
        return temizle(ad)
    except Exception:
        try:
            return temizle(Path(kok or KOK).name)
        except Exception:
            return YEDEK_AD


def yol(tur: str, kok: str | os.PathLike | None = None) -> str:
    """Env override varsa onu, yoksa /tmp/compact-<ad>-<dosya> yolunu döner."""
    env_adi, dosya = TURLER[tur]
    return os.environ.get(env_adi) or DESEN.format(ad=repo_adi(kok), dosya=dosya)


def main(argv: list[str]) -> int:
    tur = argv[1] if len(argv) > 1 else "resume"
    if tur == "ad":
        print(repo_adi())
        return 0
    if tur not in TURLER:
        print(f"kullanım: {argv[0]} [{'|'.join(TURLER)}|ad]", file=sys.stderr)
        return 2
    print(yol(tur))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
