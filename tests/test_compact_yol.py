#!/usr/bin/env python3
"""scripts/compact_yol.py — ritüel dosya yollarının repo adından türetilmesi.

NEDEN: ortak /tmp yolları aynı makinedeki projeleri karıştırıyordu (bir proje
ötekinin resume'unu "taze" sanıp okuyabiliyordu). Bu test adın doğru türediğini
ve modülün hiçbir koşulda istisna fırlatmadığını doğrular. Gerçek ritüel
dosyalarına dokunmaz: yalnız geçici dizinlerde git reposu kurar.

Kullanım:
  pytest tests/test_compact_yol.py -q
  python3 tests/test_compact_yol.py
"""
from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # hedef projede scripts/__pycache__ bırakma
ROOT = Path(__file__).resolve().parents[1]
BETIK = ROOT / "scripts" / "compact_yol.py"
FAILURES: list[str] = []
ENV_ADLARI = ("COMPACT_RESUME_PATH", "COMPACT_PREFLIGHT_PATH",
              "COMPACT_BLOCK_MARKER", "COMPACT_HISTORY_LOG")


def check(name, actual, expected):
    if actual == expected:
        print(f"ok   {name}")
    else:
        print(f"FAIL {name}: {actual!r} != {expected!r}")
        FAILURES.append(name)


def _load():
    spec = importlib.util.spec_from_file_location("compact_yol_test", BETIK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(cwd, *args):
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false",
                    "-c", "protocol.file.allow=always", "-c", "init.defaultBranch=main", *args],
                   cwd=cwd, check=True, capture_output=True, text=True, timeout=30)


def yeni_repo(ust: Path, ad: str) -> Path:
    d = ust / ad
    d.mkdir()
    git(d, "init", "-q")
    (d / "a.txt").write_text("a\n")
    git(d, "add", "a.txt")
    git(d, "commit", "-qm", "ilk")
    return d


def temiz_env() -> dict:
    return {k: v for k, v in os.environ.items() if k not in ENV_ADLARI}


yol_mod = _load()
eski_env = {k: os.environ.pop(k) for k in ENV_ADLARI if k in os.environ}
TMP = Path(tempfile.mkdtemp(prefix="crk-yol-")).resolve()
# Geçici dizinin üstündeki bir git reposu "git yok" vakasını bozmasın.
os.environ["GIT_CEILING_DIRECTORIES"] = str(TMP)
try:
    # 1. iki farklı repo adı → farklı yollar
    alfa, beta = yeni_repo(TMP, "alfa"), yeni_repo(TMP, "beta")
    check("alfa repo adı", yol_mod.repo_adi(alfa), "alfa")
    check("beta repo adı", yol_mod.repo_adi(beta), "beta")
    check("iki repo → farklı resume yolu",
          yol_mod.yol("resume", alfa) != yol_mod.yol("resume", beta), True)
    check("yol deseni", yol_mod.yol("preflight", alfa), "/tmp/compact-alfa-preflight.md")
    check("marker deseni", yol_mod.yol("marker", alfa), "/tmp/compact-alfa-block.marker")
    check("history deseni", yol_mod.yol("history", alfa), "/tmp/compact-alfa-history.log")

    # 2. bağlı worktree → ek; ana checkout → eksiz
    ana = yeni_repo(TMP, "Ana_Repo")
    git(ana, "worktree", "add", "-q", str(TMP / "ozellik-x"), "-b", "ozellik-x")
    check("ana checkout eksiz", yol_mod.repo_adi(ana), "ana-repo")
    check("worktree ekli", yol_mod.repo_adi(TMP / "ozellik-x"), "ana-repo-ozellik-x")
    (TMP / "ozellik-x" / "alt").mkdir()
    check("worktree alt dizininden de aynı ad",
          yol_mod.repo_adi(TMP / "ozellik-x" / "alt"), "ana-repo-ozellik-x")

    # 3. submodule (common-dir = .git/modules/<x>) → show-toplevel adı
    git(ana, "submodule", "add", "-q", str(alfa), "alt-modul")
    check("submodule → kendi dizin adı", yol_mod.repo_adi(ana / "alt-modul"), "alt-modul")

    # 4. git olmayan dizin → dizin adı (temizlenmiş); temizlik boşsa 'proje'
    gitsiz = TMP / "Git Yok.Dizin"
    gitsiz.mkdir()
    check("git yok → dizin adı", yol_mod.repo_adi(gitsiz), "git-yok-dizin")
    bos_ad = TMP / "!!!"
    bos_ad.mkdir()
    check("temizlik boş → proje", yol_mod.repo_adi(bos_ad), "proje")

    # 5. temizleme
    check("temizle büyük harf/nokta/alt çizgi", yol_mod.temizle("Foo_Bar.Baz"), "foo-bar-baz")
    check("temizle ardışık ayraç", yol_mod.temizle("a -- b"), "a-b")
    check("temizle boş", yol_mod.temizle(""), "proje")
    check("temizle None", yol_mod.temizle(None), "proje")

    # 6. env override'ları önceliklidir
    for tur, (env_adi, _) in yol_mod.TURLER.items():
        os.environ[env_adi] = f"/ozel/{tur}"
        check(f"env override kazanır ({env_adi})", yol_mod.yol(tur, alfa), f"/ozel/{tur}")
        os.environ.pop(env_adi)
    check("override kalkınca desen döner", yol_mod.yol("resume", alfa), "/tmp/compact-alfa-resume.md")

    # 7. git zaman aşımı / git yok → istisna yok, dizin adına düşer
    gercek_run = yol_mod.subprocess.run
    gorulen: dict = {}

    def zaman_asimi(*a, **k):
        gorulen.update(k)
        raise subprocess.TimeoutExpired(cmd="git", timeout=k.get("timeout"))

    def git_yok(*a, **k):
        raise FileNotFoundError("git")

    try:
        yol_mod.subprocess.run = zaman_asimi
        check("zaman aşımında istisna yok → dizin adı", yol_mod.repo_adi(alfa), "alfa")
        check("git çağrısı zaman aşımlı (3 sn)", gorulen.get("timeout"), 3)
        yol_mod.subprocess.run = git_yok
        check("git yokken istisna yok → dizin adı", yol_mod.repo_adi(beta), "beta")
    finally:
        yol_mod.subprocess.run = gercek_run

    # 8. CLI: kök betiğin konumundan — cwd'den bağımsız; git PATH'te yokken de çöker değil
    env = temiz_env()
    beklenen = f"/tmp/compact-{yol_mod.repo_adi()}-resume.md"
    kokten = subprocess.run([sys.executable, str(BETIK), "resume"], cwd=ROOT, env=env,
                            capture_output=True, text=True, timeout=30)
    kokten_disi = subprocess.run([sys.executable, str(BETIK), "resume"], cwd="/", env=env,
                                 capture_output=True, text=True, timeout=30)
    check("CLI kökten", kokten.stdout.strip(), beklenen)
    check("CLI cwd=/ iken aynı yol", kokten_disi.stdout.strip(), beklenen)
    check("CLI ad", subprocess.run([sys.executable, str(BETIK), "ad"], cwd="/", env=env,
                                   capture_output=True, text=True, timeout=30).stdout.strip(),
          yol_mod.repo_adi())
    gitsiz_env = dict(env, PATH="")
    r = subprocess.run([sys.executable, str(BETIK), "preflight"], cwd="/", env=gitsiz_env,
                       capture_output=True, text=True, timeout=30)
    check("CLI git PATH'te yokken exit 0", r.returncode, 0)
    check("CLI git yokken kök dizin adı", r.stdout.strip(),
          f"/tmp/compact-{yol_mod.temizle(ROOT.name)}-preflight.md")
    r = subprocess.run([sys.executable, str(BETIK), "bilinmeyen"], env=env,
                       capture_output=True, text=True, timeout=30)
    check("CLI bilinmeyen tür → exit 2", r.returncode, 2)
finally:
    os.environ.pop("GIT_CEILING_DIRECTORIES", None)
    os.environ.update(eski_env)
    shutil.rmtree(TMP, ignore_errors=True)


def test_hepsi_gecti():
    assert not FAILURES, "%d basarisiz: %s" % (len(FAILURES), FAILURES)


if __name__ == "__main__":
    if FAILURES:
        print(f"\n{len(FAILURES)} FAILED")
        sys.exit(1)
    print("\nTÜMÜ GEÇTİ")
