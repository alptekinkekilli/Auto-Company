#!/usr/bin/env bash
# Graft grafiğini üretir ve kart versiyonlama kuralını korur:
#   graft/*.md + graft/manifest.json COMMIT EDİLİR (kartlar PR'larda diff'lenebilsin diye)
#   graft/.cache/ + graft/.graph/  edilmez (makineye özgü / yeniden üretilebilir)
#
# NEDEN SARMALAYICI: `graft build` her çalıştığında .gitignore'a "graft/" satırını
# kendiliğinden geri ekliyor. Bu, kartların versiyonlanması kararını sessizce iptal eder
# (git, dışlanmış bir dizinin içeriğini negation ile geri dâhil edemez). Bu script o
# satırı build sonrası temizler.
#
# Kullanım:
#   ./.graft-kit/bin/graft-build.sh            # yapısal grafik (anahtarsız, $0)
#   ./.graft-kit/bin/graft-build.sh --deep     # + kavram kartları (LLM anahtarı gerekir)
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(git -C "$HERE" rev-parse --show-toplevel)"
cd "$ROOT"

GRAFT_VERSION="${GRAFT_VERSION:-0.10.1}"   # .mcp.json ile aynı olmalı; birlikte yükseltin
KEYCHAIN_SERVICE="${GRAFT_KEYCHAIN_SERVICE:-autocompany-together-key}"

if [[ " $* " == *" --deep "* ]]; then
  export GRAFT_PROVIDER="${GRAFT_PROVIDER:-openai}"
  export GRAFT_BASE_URL="${GRAFT_BASE_URL:-https://api.together.ai/v1}"
  export GRAFT_MODEL="${GRAFT_MODEL:-deepseek-ai/DeepSeek-V4-Flash-0731}"
  if [ -z "${GRAFT_API_KEY:-}" ]; then
    GRAFT_API_KEY="$(security find-generic-password -w -a "$USER" -s "$KEYCHAIN_SERVICE" 2>/dev/null)" || {
      echo "HATA: LLM anahtarı Keychain'de bulunamadı ($KEYCHAIN_SERVICE)." >&2
      echo "Eklemek için: security add-generic-password -a \"\$USER\" -s $KEYCHAIN_SERVICE -w" >&2
      exit 1
    }
    export GRAFT_API_KEY
  fi
fi

npx -y "@nanonets/graft@$GRAFT_VERSION" build "$@"

# Bilinen graft tuhaflığı: sembol özeti "stale" işaretlenip yeniden hesaplanmayabiliyor
# ("meaning: 0 computed, N cached, 1 stale"). --no-reuse de çözmüyor; özet cache'ini
# silmek çözüyor. --deep koşusunda kalan stale varsa bir kez temizleyip tekrar dene.
#
# SINIR — bu kurtarma "pending" durumunu ÇÖZMEZ. summaries.json kavram katmanının
# cache'idir; wiring meaning'i orada tutulmaz (NanoNets/Graft#172, maintainer teşhisi).
# Düğümler pending kalıyorsa neden modelin zorunlu tool call'u kaçırmasıdır (#129):
# res.toolCalls[0] boş dönünce crux sessizce [] üretir, build yine 0 ile çıkar.
# Çare cache silmek değil, tool call'u güvenilir üreten bir model kullanmaktır —
# bkz. docs/model-secimi.md, check-graft-model.sh ve check-graft-crux.py.
if [[ " $* " == *" --deep "* ]] && npx -y "@nanonets/graft@$GRAFT_VERSION" check 2>&1 | grep -q "stale summaries"; then
  echo "  graft: özet cache'i takıldı — temizlenip yeniden üretiliyor"
  rm -f graft/.cache/summaries.json
  npx -y "@nanonets/graft@$GRAFT_VERSION" build "$@"
fi

# --- deponun ignore kuralını geri koy ---
# Mantık gitignore-guard.py içinde; aynı temizlik hook olarak da bağlı
# (graft'ın kendi hook'ları bu sarmalayıcıyı atlayarak .gitignore'ı yazıyor).
python3 "$HERE/gitignore-guard.py" "$ROOT"

echo
echo "Commit edilecek kart dosyaları:"
git ls-files --others --modified --exclude-standard graft | sed 's/^/  /' || true
echo "Değişiklik varsa: git add graft && git commit"
