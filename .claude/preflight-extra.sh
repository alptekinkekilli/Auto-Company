#!/bin/bash
# Compact öncesi projeye özel kontroller — her ⚠ satırı bir açık kalem sayılır.
# Fail-open: hiçbir koşulda sıfır-dışı çıkma / akışı bloklama.
#
# autocompany-deploy'un dirty/unpushed/stash kontrolü BURADA tekrar yazılmıyor: onu
# zaten compact-preflight.py'nin kendi repo_report'u yapıyor (PREFLIGHT_ROOTS env'i
# .claude/settings.json'da o repoyu ekliyor) — aynı test edilmiş kodu iki kez yazmamak
# için. Burada yalnız BAŞKA hiçbir genel kontrolün yakalayamayacağı, bu projeye özgü
# şeyler var: prod konteynerinin image'i origin/main'i yakaladı mı, bu ana repo'nun
# kendisi origin/main'e PUSH edilmiş mi (2026-08-06'da tam da bu kaçırıldı — 6 commit
# yerelde kaldı, main'in tracking'i ilgisiz bir fork'a bağlıydı, git status hiç
# göstermedi; burada HER ZAMAN origin/main'e karşı açıkça ölçülür), loop hold'da mı,
# cockpit ayakta mı, operatörü bekleyen bir OPREQ var mı.
set +e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ORIGIN_MAIN=$(git -C "$REPO_ROOT" rev-parse origin/main 2>/dev/null)
UNPUSHED=$(git -C "$REPO_ROOT" log --oneline origin/main..HEAD 2>/dev/null | wc -l | tr -d ' ')
[ "${UNPUSHED:-0}" -gt 0 ] && echo "⚠ Bu repo origin/main'in ${UNPUSHED} commit İLERİSİNDE — PUSH EDİLMEMİŞ (bir redeploy bunları görmeyecek, git push origin main)"

SSH_OUT=$(ssh -o BatchMode=yes -o ConnectTimeout=8 powerupp-ts '
C=$(docker ps --format "{{.Names}}" | grep z12a992 | head -1)
if [ -z "$C" ]; then echo "CONTAINER=NONE"; exit 0; fi
IMG=$(docker inspect --format "{{.Config.Image}}" "$C" 2>/dev/null)
echo "CONTAINER=$C"
echo "IMAGE=$IMG"
docker exec -u app "$C" sh -c "
  cd /app || exit 0
  if [ -f logs/LOOP_HOLD ]; then
    echo HOLD=HELD:\$(sed -n \"2p\" logs/LOOP_HOLD)
  else
    echo HOLD=released
  fi
  # state-snapshot.py state dosyasini YAZAR ve DELTA tuketir - loop bir sonraki
  # cycle degisikligi goremez olur; cevresinde save/restore zorunlu.
  # 2026-08-24: KARAR-001 deltasini bu satir iki kez tuketti.
  cp logs/state-snapshot-last.json /tmp/ss-preflight-bak 2>/dev/null
  timeout 6 python3 scripts/ops/state-snapshot.py --app /app 2>/dev/null | grep -E \"^opreq:\"
  [ -f /tmp/ss-preflight-bak ] && mv /tmp/ss-preflight-bak logs/state-snapshot-last.json
  echo COCKPIT=\$(curl -s -o /dev/null -w \"%{http_code}\" -m5 http://127.0.0.1:8787/api/status)
"
' 2>/dev/null)

field() { printf '%s\n' "$SSH_OUT" | grep -m1 "^$1=" | cut -d= -f2-; }
# state-snapshot.py satırları "anahtar: değer" biçiminde (= değil) — ayrı çekici.
rawline() { printf '%s\n' "$SSH_OUT" | grep -m1 "^$1:"; }

if [ -z "$SSH_OUT" ]; then
  echo "⚠ Prod sunucusuna ulaşılamadı (Tailscale/ssh?) — konteyner/hold/cockpit durumu DOĞRULANMADI"
else
  CONTAINER=$(field CONTAINER)
  if [ "$CONTAINER" = "NONE" ] || [ -z "$CONTAINER" ]; then
    echo "⚠ Prod konteyneri BULUNAMADI (z12a992*) — beklenmedik durum"
  else
    IMGSHA=$(field IMAGE | cut -d: -f2)
    if [ -n "$IMGSHA" ] && [ -n "$ORIGIN_MAIN" ] && git -C "$REPO_ROOT" cat-file -e "$IMGSHA" 2>/dev/null; then
      IMG_VS_ORIGIN=$(git -C "$REPO_ROOT" log --oneline "${IMGSHA}..${ORIGIN_MAIN}" 2>/dev/null | wc -l | tr -d ' ')
      if [ "${IMG_VS_ORIGIN:-0}" -gt 0 ]; then
        echo "⚠ Prod image origin/main'in ${IMG_VS_ORIGIN} commit GERİSİNDE (taban ${IMGSHA:0:12}) — o commitlerden sonraki her canlı-yama (docker exec/tar) KAYBOLMUŞ olabilir; redeploy gerekir"
      fi
    else
      echo "⚠ Prod image tabanı DOĞRULANAMADI (${IMGSHA:-boş}) — origin/main'e göre drift ölçülemedi"
    fi

    HOLD=$(field HOLD)
    case "$HOLD" in
      HELD:*) echo "⚠ Loop HOLD durumunda (${HOLD#HELD:}) — kapatmadan önce operatörün bilerek mi bıraktığını doğrula" ;;
    esac

    CC=$(field COCKPIT)
    [ "$CC" != "200" ] && echo "⚠ Cockpit sağlıksız (HTTP ${CC:-yok})"

    OQ=$(rawline opreq | grep -oE 'open=[0-9]+' | cut -d= -f2)
    [ "${OQ:-0}" -gt 0 ] && echo "⚠ Operatörü bekleyen açık OPREQ: $OQ (cockpit \"Requests to you\" paneli)"
  fi
fi

PA="$(dirname "$0")/pending-actions.md"
if [ -f "$PA" ]; then
  grep -E "^- \[ \]" "$PA" 2>/dev/null | sed 's/^- \[ \]/⚠ BEKLEYEN:/'
fi

exit 0
