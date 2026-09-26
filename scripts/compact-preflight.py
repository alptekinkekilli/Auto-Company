#!/usr/bin/env python3
"""Compact ön-kontrolü — PreCompact hook'undan (manual VE auto) otomatik koşar.

NEDEN: compact ritüeli "kullanıcı haber verir + ajan hatırlar" varsayımına dayanır.
İki delik: otomatik compact haber vermez, hatırlama garanti değildir. Bu betik
ritüelin ÖLÇÜLEBİLİR kısmını koda çevirir — kaybolursa acıtacak şeyleri sayar.

Çıktı iki yere gider: stdout (hook günlüğü) ve ön-kontrol dosyası
(`python3 scripts/compact_yol.py preflight`) — compact SONRASI session-brief bunu
okuyup açık kalemleri yeni bağlama taşır.

RESUME DOSYASI (v4): ritüelin kanonik resume'u sohbet mesajı DEĞİL, dosyadır
(`python3 scripts/compact_yol.py resume` — repo adına özel yol; şablon
.claude/skills/compact-ritual/resume-template.md).
Sohbet metni özetleyicinin insafına kalır; dosya compact'ten etkilenmez. Bu betik
resume'un TAZE olduğunu doğrular ve otomatik compact'i resume hazır değilken BİR
KEZ erteleyebilir (aşağıda).

TAZE ≠ mtime (v5): dosyaya dokunulmuş olması içeriğin sağlam olduğunu göstermez —
canlı kullanımda mtime'ı taze ama zorunlu bölümü eksik resume sessizce geçiyordu.
"Taze" artık iki koşulun BİRLİKTE sağlanmasıdır: mtime < 3 saat VE
compact-resume-lint.py yeşil.

Genişletme: PREFLIGHT_ROOTS env'i ile ek git kökleri (iki nokta üst üste ayrılmış)
taranır. Projeye özel kontroller için .claude/preflight-extra.sh (çalıştırılabilir)
varsa koşulur ve çıktısı rapora eklenir — betiği fork'lamana gerek yok.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys

# Yollar repo adına özeldir ve tek kaynaktan gelir (scripts/compact_yol.py).
# Dosya yoluyla yüklenir: testler betiği importlib ile yüklese de çalışsın.
# dont_write_bytecode: hedef projede izlenmeyen scripts/__pycache__ bırakılmasın.
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compact_yol  # noqa: E402

# COMPACT_PREFLIGHT_PATH/COMPACT_RESUME_PATH/COMPACT_BLOCK_MARKER env'leri
# testlerin sandbox'a yönlendirmesi içindir; gerçek kullanımda set edilmez.
OUT = compact_yol.yol("preflight")
RESUME = compact_yol.yol("resume")
MARKER = compact_yol.yol("marker")
RESUME_TAZE_SAAT = 3
MARKER_TTL_DK = 30


def sh(args, cwd=None):
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


def hook_payload() -> dict:
    """PreCompact hook'u stdin'den JSON verir (trigger: manual|auto, session_id...).
    Elle koşulduğunda stdin boş/tty'dir — {} döner ve erteleme yolu hiç açılmaz."""
    try:
        if sys.stdin.isatty():
            return {}
        raw = sys.stdin.read()
        return json.loads(raw) if raw.strip() else {}
    except Exception:
        return {}


def resume_lint_gecer_mi() -> tuple[bool, str]:
    """compact-resume-lint.py'yi subprocess ile koşar; exit 0 = içerik yeşil.

    NEDEN AYRI ÇAĞRI: lint kuralları tek dosyada (compact-resume-lint.py) yaşar;
    burada kopyalanırsa iki kural seti sessizce ayrışır. Mekanik kapı içerik
    doğrulamadan "taze" diyemez — mtime yalnız dokunulmayı ölçer, sağlamlığı değil.
    """
    betik = os.path.join(os.path.dirname(os.path.abspath(__file__)), "compact-resume-lint.py")
    try:
        r = subprocess.run([sys.executable, betik, RESUME], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            return True, "lint yeşil"
        ilk_hata = next((s.strip() for s in r.stdout.splitlines() if s.strip().startswith("✗")),
                        r.stdout.strip()[:100] or "lint kırmızı (çıktı boş)")
        return False, ilk_hata
    except Exception as e:
        return False, f"lint çalıştırılamadı ({e})"


def resume_durumu() -> tuple[bool, str]:
    try:
        yas_sa = (dt.datetime.now().timestamp() - os.path.getmtime(RESUME)) / 3600
    except OSError:
        return False, "resume dosyası YOK"
    if yas_sa > RESUME_TAZE_SAAT:
        return False, f"resume BAYAT ({yas_sa:.1f} sa > {RESUME_TAZE_SAAT} sa)"
    lint_ok, lint_mesaj = resume_lint_gecer_mi()
    if not lint_ok:
        return False, f"resume mtime taze ({yas_sa:.1f} sa) ama LINT KIRMIZI: {lint_mesaj}"
    return True, f"resume taze ({yas_sa:.1f} sa) + lint yeşil"


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
    now = dt.datetime.now()
    payload = hook_payload()
    roots = [os.getcwd()] + [r for r in os.environ.get("PREFLIGHT_ROOTS", "").split(":") if r]
    L = [f"# Compact ön-kontrolü — {now.strftime('%Y-%m-%d %H:%M')}", ""]
    risk = 0
    for r in roots:
        s, x = repo_report(r)
        L += s
        risk += x

    # RESUME DOSYASI: yok/bayat/lint-kırmızıysa bu compact karar metnini yalnız
    # özetleyicinin insafına bırakır — açık kalem olarak işaretlenir.
    taze, aciklama = resume_durumu()
    if not taze:
        risk += 1
        L.append(f"- ⚠ RESUME DOSYASI: {aciklama} — ritüelin resume adımı çalışmamış; "
                 f"şablon .claude/skills/compact-ritual/resume-template.md → {RESUME}, "
                 f"doğrulama scripts/compact-resume-lint.py")

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

    # OTOMATİK compact'i BİR KEZ ertele: canlı kullanımda iki compact üst üste,
    # ritüel resume'u teslim edemeden araya girdi — resume yalnız sohbetteydi.
    # Kural: yalnız trigger=="auto" + resume taze değil + marker bayatken; ikinci
    # deneme DAİMA geçer (sert bağlam limitinde bloklamak hatayı yüzeye çıkarır,
    # dokümante risk). Manuel /compact ASLA bloklanmaz — kullanıcı iradesi üstündür.
    # Kapatma anahtarı: COMPACT_AUTOBLOCK=0.
    if (payload.get("trigger") == "auto" and not taze
            and os.environ.get("COMPACT_AUTOBLOCK", "1") != "0"):
        marker_taze = False
        try:
            marker_taze = (now.timestamp() - os.path.getmtime(MARKER)) / 60 < MARKER_TTL_DK
        except OSError:
            pass
        if not marker_taze:
            try:
                open(MARKER, "w").write(now.isoformat())
            except Exception:
                pass
            # Bloklarken stdout SADECE karar JSON'u olmalı — markdown karışırsa
            # JSON parse edilemez ve karar düz metin sanılıp yok sayılır.
            print(json.dumps({"decision": "block", "reason": (
                f"Otomatik compact BİR KEZ ertelendi: {aciklama}. ŞİMDİ ritüelin "
                f"resume adımını uygula — şablondan "
                f"(.claude/skills/compact-ritual/resume-template.md) {RESUME} dosyasına "
                f"YAZ ve scripts/compact-resume-lint.py ile doğrula; bir sonraki "
                f"otomatik compact serbest geçer ({MARKER_TTL_DK} dk marker). "
                f"Açık kalemler: {OUT}")}))
            return 0

    print(metin)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
