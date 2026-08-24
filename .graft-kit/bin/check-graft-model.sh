#!/usr/bin/env bash
# GRAFT_MODEL'in graft --deep için uygun olup olmadığını doğrular.
#
# Graft'ın synthesize pass'i ZORUNLU tool calling kullanır. Model bunu
# desteklemiyorsa --deep başarısız olur. Bu script anahtar harcamadan
# (tek küçük istek) bunu önceden test eder.
#
# Kullanım:
#   GRAFT_API_KEY="$(security find-generic-password -w -a "$USER" -s autocompany-together-key)" \
#     bash shared/scripts/check-graft-model.sh
#
# Anahtar argv'ye YAZILMAZ; yalnızca environment üzerinden okunur.
set -euo pipefail

BASE="${GRAFT_BASE_URL:-https://api.together.ai/v1}"
MODEL="${GRAFT_MODEL:-deepseek-ai/DeepSeek-V4-Flash-0731}"

[ -n "${GRAFT_API_KEY:-}" ] || {
  echo "HATA: GRAFT_API_KEY tanımlı değil." >&2
  echo "Örn: GRAFT_API_KEY=\"\$(security find-generic-password -w -a \"\$USER\" -s autocompany-together-key)\" $0" >&2
  exit 1
}

echo "Endpoint : $BASE"
echo "Model    : $MODEL"
echo

TMP="$(mktemp -t graftprobe)"
trap 'rm -f "$TMP"' EXIT

# Şema, graft'ın gerçek record_graph aracını taklit eder: iç içe dizi + enum + zorunlu
# alanlar. Basit düz şema yanıltıcıdır — bazı modeller onu geçip gerçek şemada çöker.
curl -sS -o "$TMP" -X POST "$BASE/chat/completions" \
  -H "Authorization: Bearer $GRAFT_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- <<JSON
{
  "model": "$MODEL",
  "temperature": 0,
  "max_tokens": 600,
  "messages": [{"role":"user","content":"Files: render.py (turns templates into PNG via headless Chrome), config.json (single source of texts and values), scaffold.sh (creates a new project skeleton). Record the concept graph."}],
  "tools": [{
    "type": "function",
    "function": {
      "name": "record_graph",
      "description": "Record the concept graph for a set of source files.",
      "parameters": {
        "type": "object",
        "properties": {
          "nodes": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "name":    {"type": "string"},
                "kind":    {"type": "string", "enum": ["subsystem", "file", "concept"]},
                "summary": {"type": "string"},
                "links":   {"type": "array", "items": {"type": "string"}}
              },
              "required": ["name", "kind", "summary"]
            }
          }
        },
        "required": ["nodes"]
      }
    }
  }],
  "tool_choice": {"type": "function", "function": {"name": "record_graph"}}
}
JSON

python3 - "$MODEL" "$TMP" <<'PY'
import json, sys
model = sys.argv[1]
raw = open(sys.argv[2], encoding="utf-8").read()
try:
    d = json.loads(raw)
except Exception:
    print("BAŞARISIZ — yanıt JSON değil:\n" + raw[:400]); sys.exit(1)

if "error" in d:
    msg = d["error"].get("message", d["error"]) if isinstance(d["error"], dict) else d["error"]
    print(f"BAŞARISIZ — sağlayıcı hatası:\n  {msg}")
    if "non-serverless" in str(msg) or "model_not_available" in raw:
        print("\n  -> Bu model SERVERLESS DEĞİL; dedicated endpoint gerektiriyor. Kullanmayın.")
    else:
        print("\n  -> Model id yanlış olabilir veya hesabınızda erişilebilir değil.")
    print("  Test edilmiş alternatifler: deepseek-ai/DeepSeek-V4-Flash-0731, openai/gpt-oss-120b")
    sys.exit(1)

calls = (d.get("choices") or [{}])[0].get("message", {}).get("tool_calls")
u = d.get("usage") or {}
if calls:
    try:
        args = json.loads(calls[0]["function"].get("arguments") or "{}")
    except Exception as e:
        print(f"UYGUN DEĞİL — {model} tool_calls döndürdü ama arguments geçersiz JSON: {e}")
        sys.exit(1)
    nodes = args.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        print(f"UYGUN DEĞİL — {model} 'nodes' dizisi üretmedi (şemaya uymuyor).")
        sys.exit(1)
    bad = [n for n in nodes if not all(k in n for k in ("name", "kind", "summary"))]
    if bad:
        print(f"UYGUN DEĞİL — {model} zorunlu alanları eksik düğüm üretti ({len(bad)}/{len(nodes)}).")
        sys.exit(1)
    print(f"UYGUN — {model} iç içe şemaya uygun {len(nodes)} düğüm üretti.")
    print(f"  örnek: [{nodes[0]['kind']}] {nodes[0]['name']} — {nodes[0]['summary'][:70]}")
    if u:
        print(f"  usage: girdi {u.get('prompt_tokens','?')} / çıktı {u.get('completion_tokens','?')} token")
    print("\ngraft build --deep bu modelle çalıştırılabilir.")
else:
    print(f"UYGUN DEĞİL — {model} tool_calls döndürmedi; graft --deep bu modelle çalışmaz.")
    content = (d.get("choices") or [{}])[0].get("message", {}).get("content") or ""
    if content.strip().startswith("{"):
        print("  (Model doğru JSON üretti ama tool_calls yerine content'e yazdı —")
        print("   graft res.toolCalls[0] okuduğu için bu çalışmaz. Ör: Ternary-Bonsai-27B.)")
    print("  Test edilmiş alternatifler: deepseek-ai/DeepSeek-V4-Flash-0731, openai/gpt-oss-120b")
    sys.exit(1)
PY
