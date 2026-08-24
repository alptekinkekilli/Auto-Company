#!/usr/bin/env python3
"""
Claude Code oturum transcript'lerinden görev bazlı metrik çıkarır.

Amaç: "graft'lı / graft'sız" farkını iddia etmek yerine ÖLÇMEK. Claude Code her
oturumu JSONL olarak yazar; bu script onu okuyup her kullanıcı görevi için tool
call sayısı, token tüketimi ve duvar saati süresini çıkarır.

Kullanım:
    python3 shared/scripts/metrics.py                 # son oturum, tablo
    python3 shared/scripts/metrics.py --summary       # yalnızca toplamlar
    python3 shared/scripts/metrics.py --append        # metrics/tasks.jsonl'a ekle
    python3 shared/scripts/metrics.py --file <path>   # belirli bir transcript

NE ÖLÇER
    tool_calls      görevde yapılan tool çağrısı sayısı (araç bazında kırılımlı)
    explore_calls   keşif çağrıları: Read / Grep / Glob (görseldeki "wanders the repo")
    graft_read      grafikten bağlam çekme (ask/grep/callers/map + MCP araçları)
    graft_ops       graft kurulum/build/check — bağlam getirme DEĞİL, ayrı sayılır
    out_tokens      üretilen token (en pahalı kalem, 1.0x)
    in_fresh        cache'lenmemiş girdi token'ı (1.0x)
    cache_read      cache'ten okunan girdi (~0.1x — ayrı raporlanır, toplanmaz)
    seconds         görevin ilk ve son kaydı arasındaki süre

BİLİNEN SINIR — tool call birimi
    Tek bir Bash çağrısında birden fazla komut çalıştırılabilir; sayaç komutu değil
    TOOL CALL'u sayar. Bu, görseldeki "%46 daha az tool call" metriğiyle aynı birimdir,
    ama graft komutlarını batch'lerseniz graft olduğundan verimli görünür.

NE ÖLÇMEZ — dürüstlük notu
    Bu GÖZLEMSEL bir ölçümdür, kontrollü A/B değildir. Görevler birbirinden farklı
    büyüklükte olduğu için iki görevi doğrudan karşılaştırmak yanıltıcıdır. Anlamlı
    karşılaştırma için aynı görevi graft açık/kapalı çalıştırmak gerekir
    (bkz. docs/olcum-plani.md).
"""

import argparse
import json
import subprocess
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())

# Keşif araçları — görseldeki "wanders the repo" adımının karşılığı
EXPLORE = {"Read", "Grep", "Glob"}
# Bash içinde keşif sayılan komutlar
BASH_EXPLORE = re.compile(r"\b(grep|rg|find|cat|head|tail|sed -n|ls)\b")
# graft BAĞLAM GETİRME komutları — görseldeki "read the graph" adımı
GRAFT_READ = re.compile(r"\bgraft(@[\w.]+)?\s+(ask|grep|callers|skeleton|map|viz)\b")
# graft KURULUM/BAKIM komutları — ölçümde bağlam getirme sayılmamalı
GRAFT_OPS = re.compile(r"\bgraft(@[\w.]+)?\s+(init|build|check|mcp)\b|graft-build\.sh|check-graft-model\.sh")


def transcript_dir() -> Path:
    slug = str(ROOT).replace("/", "-")
    return Path.home() / ".claude" / "projects" / slug


def latest_transcript() -> Path:
    d = transcript_dir()
    files = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        sys.exit(f"HATA: transcript bulunamadı: {d}")
    return files[0]


def ts(rec: dict):
    t = rec.get("timestamp")
    if not t:
        return None
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00"))
    except ValueError:
        return None


def graft_kind(name: str, block: dict):
    """'read' = grafikten bağlam çekme, 'ops' = kurulum/bakım, None = graft değil.

    Ayrım şart: `npx graft build` çalıştırmak bağlam getirmek DEĞİLDİR. İkisini
    tek sayaçta toplamak graft'ın işe yarama oranını olduğundan yüksek gösterir.
    """
    if name.startswith("mcp__graft__"):
        return "ops" if name.endswith("check_freshness") else "read"
    if name == "Bash":
        cmd = (block.get("input") or {}).get("command", "")
        if GRAFT_READ.search(cmd):
            return "read"
        if GRAFT_OPS.search(cmd) or "@nanonets/graft" in cmd:
            return "ops"
    return None


def parse(path: Path) -> list:
    tasks, cur = [], None

    def close():
        if cur and (cur["tool_calls"] or cur["out_tokens"]):
            tasks.append(cur)

    for line in path.open(encoding="utf-8"):
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue

        typ = rec.get("type")

        # Yeni görev: düz metin kullanıcı mesajı. tool_result'lar görev değildir.
        if typ == "user":
            content = rec.get("message", {}).get("content")
            text = None
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                parts = [b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text"]
                if parts:
                    text = " ".join(parts)
            if text and text.strip():
                close()
                t = ts(rec)
                cur = {
                    "prompt": " ".join(text.split())[:80],
                    "start": t, "end": t,
                    "tool_calls": 0, "explore_calls": 0,
                    "graft_read": 0, "graft_ops": 0,
                    "tools": Counter(),
                    "out_tokens": 0, "in_fresh": 0, "cache_read": 0, "cache_write": 0,
                    "turns": 0,
                }
            continue

        if typ != "assistant" or cur is None:
            continue

        cur["turns"] += 1
        t = ts(rec)
        if t:
            cur["end"] = t

        u = rec.get("message", {}).get("usage") or {}
        cur["out_tokens"] += u.get("output_tokens", 0) or 0
        cur["in_fresh"] += u.get("input_tokens", 0) or 0
        cur["cache_read"] += u.get("cache_read_input_tokens", 0) or 0
        cur["cache_write"] += u.get("cache_creation_input_tokens", 0) or 0

        for b in rec.get("message", {}).get("content") or []:
            if not isinstance(b, dict) or b.get("type") != "tool_use":
                continue
            name = b.get("name", "?")
            cur["tool_calls"] += 1
            cur["tools"][name] += 1
            gk = graft_kind(name, b)
            if gk:
                cur["graft_" + gk] += 1
            elif name in EXPLORE:
                cur["explore_calls"] += 1
            elif name == "Bash" and BASH_EXPLORE.search((b.get("input") or {}).get("command", "")):
                cur["explore_calls"] += 1

    close()
    return tasks


def secs(task) -> float:
    if task["start"] and task["end"]:
        return (task["end"] - task["start"]).total_seconds()
    return 0.0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", help="transcript yolu (varsayılan: en son oturum)")
    ap.add_argument("--summary", action="store_true", help="yalnızca toplamlar")
    ap.add_argument("--append", action="store_true",
                    help="metrics/tasks.jsonl dosyasına ekle (uzun vadeli izleme)")
    a = ap.parse_args()

    path = Path(a.file) if a.file else latest_transcript()
    tasks = parse(path)
    if not tasks:
        sys.exit("Transcript'te ölçülebilir görev bulunamadı.")

    if not a.summary:
        print(f"transcript: {path.name}   ({len(tasks)} görev)\n")
        print(f"{'#':>3}  {'araç':>5} {'keşif':>6} {'g.oku':>6} {'g.bak':>6} "
              f"{'çıktı tok':>10} {'taze gir':>9} {'cache':>9} {'sn':>7}  görev")
        print("-" * 118)
        for i, t in enumerate(tasks, 1):
            print(f"{i:>3}  {t['tool_calls']:>5} {t['explore_calls']:>6} {t['graft_read']:>6} {t['graft_ops']:>6} "
                  f"{t['out_tokens']:>10,} {t['in_fresh']:>9,} {t['cache_read']:>9,} "
                  f"{secs(t):>7.0f}  {t['prompt'][:44]}")
        print()

    n = len(tasks)
    tot = {k: sum(t[k] for t in tasks)
           for k in ("tool_calls", "explore_calls", "graft_read", "graft_ops",
                     "out_tokens", "in_fresh", "cache_read", "cache_write")}
    total_secs = sum(secs(t) for t in tasks)
    with_graft = [t for t in tasks if t["graft_read"]]

    print(f"TOPLAM ({n} görev)")
    print(f"  tool call            {tot['tool_calls']:>10,}   "
          f"(görev başına {tot['tool_calls']/n:.1f})")
    print(f"    keşif (Read/Grep)  {tot['explore_calls']:>10,}")
    print(f"    graft bağlam       {tot['graft_read']:>10,}   grafikten okuma")
    print(f"    graft bakım        {tot['graft_ops']:>10,}   kurulum/build/test (bağlam değil)")
    print(f"  çıktı token          {tot['out_tokens']:>10,}   1.0x maliyet")
    print(f"  taze girdi token     {tot['in_fresh']:>10,}   1.0x maliyet")
    print(f"  cache okuma          {tot['cache_read']:>10,}   ~0.1x maliyet")
    print(f"  cache yazma          {tot['cache_write']:>10,}   ~1.25x maliyet")
    print(f"  süre                 {total_secs/60:>10.0f} dk")
    print(f"  graft'tan bağlam alan görev {len(with_graft):>3} / {n}")

    print("\n  NOT: Bu gözlemsel bir kayıttır, kontrollü A/B değildir. Görevler farklı")
    print("  büyüklükte olduğu için görevler arası doğrudan karşılaştırma yanıltıcıdır.")

    if a.append:
        out = ROOT / "metrics"
        out.mkdir(exist_ok=True)
        f = out / "tasks.jsonl"
        seen = set()
        if f.exists():
            for line in f.open(encoding="utf-8"):
                try:
                    seen.add(json.loads(line)["key"])
                except (json.JSONDecodeError, KeyError):
                    pass
        added = 0
        with f.open("a", encoding="utf-8") as fh:
            for i, t in enumerate(tasks, 1):
                key = f"{path.stem}:{i}"
                if key in seen:
                    continue
                fh.write(json.dumps({
                    "key": key,
                    "session": path.stem,
                    "index": i,
                    "started": t["start"].isoformat() if t["start"] else None,
                    "prompt": t["prompt"],
                    "turns": t["turns"],
                    "tool_calls": t["tool_calls"],
                    "explore_calls": t["explore_calls"],
                    "graft_read": t["graft_read"],
                    "graft_ops": t["graft_ops"],
                    "tools": dict(t["tools"]),
                    "out_tokens": t["out_tokens"],
                    "in_fresh": t["in_fresh"],
                    "cache_read": t["cache_read"],
                    "cache_write": t["cache_write"],
                    "seconds": round(secs(t), 1),
                }, ensure_ascii=False) + "\n")
                added += 1
        print(f"\n  metrics/tasks.jsonl: {added} yeni kayıt eklendi "
              f"({len(seen)} zaten vardı)")


if __name__ == "__main__":
    main()
