#!/usr/bin/env python3
"""GRAFT_MODEL'in graft'ın MEANING (crux) katmanı için uygun olduğunu doğrular.

NEDEN AYRI BİR PROBE: `check-graft-model.sh` yalnızca synthesize şemasını test eder
(iç içe dizi + enum). Graft'ın ikinci tool calling yolu olan ChatCruxSummarizer farklı
ve daha düz bir şema kullanır. NanoNets/Graft#172 sırasında ölçtük: kaçırma oranı
modelden çok ŞEMA BİÇİMİNE bağlı — synthesize şemasında kaçıran bir model crux
şemasında kaçırmayabiliyor. İki kapı ayrı ayrı test edilmelidir.

İstek dist/ai/crux.js ile birebir aynıdır: aynı sistem promptu, aynı SYMBOLS_SCHEMA,
temperature 0, max_tokens 8192, zorunlu tool_choice. Hedef sayısı değiştirilebilir
çünkü describeFile DOSYA BAŞINA çağrılır; pratikte değişen budur.

İki sessiz boş-sonuç yolunu ayırır:
  TOOLCALL_YOK  — model tool call üretmedi (graft: res.toolCalls[0] undefined -> [])
  ARGS_BOZUK    — tool call geldi ama arguments bozuk JSON (graft: catch -> {} -> [])
Her ikisi de graft'ta sessizce boş sonuç verir ve build yine 0 ile çıkar.

Kullanım:
  GRAFT_API_KEY="$(security find-generic-password -w -a "$USER" -s autocompany-together-key)" \\
    python3 shared/scripts/check-graft-crux.py [hedef_sayilari] [tekrar]
  # örn: ... check-graft-crux.py 1,3,10 8

Anahtar yalnızca ortamdan okunur; argv'ye YAZILMAZ.
Cloudflare Python urllib'i engellediği için istek curl ile atılır.
"""
import json, os, subprocess, sys

SYSTEM = ("You explain code definitions for a code graph that helps engineers navigate a codebase.\n\n"
"You are given ONE source file with 1-based line numbers, and a list of TARGET definitions in it. "
"For every target, record its purpose and the line range of its core logic via the record_symbols tool.\n\n"
"Rules:\n"
"- Emit exactly one entry per target id given, using that id verbatim.\n"
"- summary: ONE sentence — what the symbol is FOR at the business-logic level. Say what problem it solves "
"or rule it enforces, not what its signature already says.\n"
"- crux_start / crux_end: FILE line numbers (as shown), inside that symbol's own line range. Pick the SINGLE "
"most important contiguous span — the core branch, formula, guard, or state change. Keep it TIGHT: at most "
"~8 lines, and NEVER the whole function. If you can't narrow it below that, the symbol has no distinct crux "
"— use 0/0.\n"
"- Skip boilerplate, logging, and plumbing. If a symbol has no meaningful crux (trivial getter, data holder, "
"one-line delegation, or logic spread evenly with no focal point), use \"crux_start\": 0 and \"crux_end\": 0.")

SCHEMA = {"type":"object","properties":{"symbols":{"type":"array","items":{"type":"object","properties":{
    "id":{"type":"string"},"summary":{"type":"string"},
    "crux_start":{"type":"number"},"crux_end":{"type":"number"}},
    "required":["id","summary","crux_start","crux_end"]}}},"required":["symbols"]}


def make_module(n):
    """n fonksiyonluk Python kaynağı + hedef listesi üretir (issue'daki minimal repro şekli)."""
    lines, targets = [], []
    for i in range(1, n + 1):
        start = len(lines) + 1
        lines += [
            f"def rule_{i}(amount, tier):",
            f'    """Apply pricing rule {i}."""',
            f"    if tier == {i}:",
            f"        return amount * {1 + i / 10:.1f}",
            "    return amount",
            "",
        ]
        targets.append({"id": f"rule_{i}", "kind": "function",
                        "startLine": start, "endLine": start + 4,
                        "signature": f"def rule_{i}(amount, tier)"})
    return "\n".join(lines), targets


def user_content(path, source, targets):
    numbered = "\n".join(f"{i+1}\t{l}" for i, l in enumerate(source.split("\n")))
    tgt = "\n".join(f"- id={t['id']} | {t['kind']} | lines L{t['startLine']}-L{t['endLine']} | {t['signature']}"
                    for t in targets)
    return f"FILE: {path}\n\n{numbered}\n\nTARGETS:\n{tgt}"


def call(model, base, key, n):
    source, targets = make_module(n)
    body = {"model": model, "temperature": 0, "max_tokens": 8192,
            "messages": [{"role": "system", "content": SYSTEM},
                         {"role": "user", "content": user_content("pricing.py", source, targets)}],
            "tools": [{"type": "function", "function": {
                "name": "record_symbols",
                "description": "Record each target definition's purpose and crux line range.",
                "parameters": SCHEMA}}],
            "tool_choice": {"type": "function", "function": {"name": "record_symbols"}}}
    p = subprocess.run(
        ["curl", "-sS", "-X", "POST", f"{base}/chat/completions",
         "-H", f"Authorization: Bearer {key}", "-H", "Content-Type: application/json", "-d", "@-"],
        input=json.dumps(body), capture_output=True, text=True, timeout=180)
    try:
        r = json.loads(p.stdout)
    except json.JSONDecodeError:
        return {"outcome": "HTTP_HATA", "detail": p.stdout[:120]}
    if "error" in r:
        return {"outcome": "API_HATA", "detail": str(r["error"])[:120]}
    msg = (r.get("choices") or [{}])[0].get("message") or {}
    finish = (r.get("choices") or [{}])[0].get("finish_reason")
    calls = [c for c in (msg.get("tool_calls") or []) if c.get("type") == "function"]
    if not calls:                                   # yol 1: toolCalls boş
        return {"outcome": "TOOLCALL_YOK", "finish": finish,
                "content_len": len(msg.get("content") or ""), "requested": n, "got": 0}
    raw = calls[0]["function"].get("arguments") or ""
    try:
        args = json.loads(raw or "{}")
    except json.JSONDecodeError:                    # yol 2: arguments bozuk JSON
        return {"outcome": "ARGS_BOZUK", "finish": finish, "raw_len": len(raw), "requested": n, "got": 0}
    syms = args.get("symbols")
    if not isinstance(syms, list):
        return {"outcome": "SYMBOLS_YOK", "finish": finish, "requested": n, "got": 0}
    ok = [s for s in syms if isinstance(s.get("id"), str)]
    ids = {s["id"] for s in ok}
    missing = [t["id"] for t in targets if t["id"] not in ids]
    return {"outcome": "TAM" if not missing else "EKSIK", "finish": finish,
            "requested": n, "got": len(ok), "missing": len(missing)}


def main():
    key = os.environ.get("GRAFT_API_KEY")
    if not key:
        sys.exit("GRAFT_API_KEY tanımlı değil.")
    model = os.environ.get("GRAFT_MODEL", "deepseek-ai/DeepSeek-V4-Flash-0731")
    base = os.environ.get("GRAFT_BASE_URL", "https://api.together.ai/v1")
    counts = [int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else "1,3,10").split(",")]
    reps = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    print(f"model: {model}\nhedef sayısı: {counts}  tekrar: {reps}\n")
    for n in counts:
        outcomes = []
        for _ in range(reps):
            outcomes.append(call(model, base, key, n))
        tam = sum(1 for o in outcomes if o["outcome"] == "TAM")
        print(f"N={n:>2}  TAM {tam}/{reps}")
        for o in outcomes:
            if o["outcome"] != "TAM":
                print(f"      ✗ {o}")
    print()


if __name__ == "__main__":
    main()
