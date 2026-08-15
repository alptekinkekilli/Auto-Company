#!/bin/bash
# Oturum brifingine eklenen projeye özel CANLI ölçümler (sayılar buradan gelir, özetten değil).
# Fail-open: hata durumunda sessizce eksik bırak, asla sıfır-dışı çıkma.
#
# Bu projede en çok acıtan sessiz kayıp biçimi (canlı yaşandı, 2026-08-06): prod
# konteynerine `docker exec`+tar ile canlı yama yapılır (hold->sync->restart->release
# ritüeli), ama görüntü asla yeniden build edilmez — yama yalnız konteynerin yazılabilir
# katmanında yaşar. Konteyner YENİDEN YARATILIRSA (Coolify redeploy, restart policy,
# health-check), yeni imaj `origin/main`'den build edilir; o gün commit edilmiş ama
# PUSH EDİLMEMİŞ hiçbir şey imaja giremez. Görüntü etiketi build edildiği git commit'i
# taşıdığı için (`<proje>:<git-sha>`), üç ayrı sayı ölçülür — hangisinin kırıldığını
# ayırt etmek için: imaj vs origin/main (deploy pipeline'ı yakaladı mı) ve local HEAD
# vs origin/main (push edilmemiş var mı — bugünkü kaybın gerçek nedeni buydu).
# `main`'in upstream tracking'i bir ara yanlış bir fork'a bağlıydı (`upstream/main`,
# ilgisiz bir repo) — bu yüzden git status bunu hiç göstermiyordu; burada HER ZAMAN
# `origin/main`'e karşı açıkça ölçülür, tracking'e güvenilmez.
#
# YEREL `origin/main` referansı kullanılır (fetch YOK, ağ çağrısı yok, ~0 sn): bu
# makineden yapılan her `git push` o referansı zaten güncelliyor, ki asıl yakalanmak
# istenen tam olarak "bu makineden push edilmedi" durumu — taze bir fetch bunu
# gizlemez, gereksiz ağ gecikmesi eklerdi.
set +e

SSH_OUT=$(ssh -o BatchMode=yes -o ConnectTimeout=8 powerupp-ts '
C=$(docker ps --format "{{.Names}}" | grep z12a992 | head -1)
if [ -z "$C" ]; then echo "CONTAINER=NONE"; exit 0; fi
IMG=$(docker inspect --format "{{.Config.Image}}" "$C" 2>/dev/null)
CREATED=$(docker inspect --format "{{.Created}}" "$C" 2>/dev/null | cut -c1-19)
echo "CONTAINER=$C"
echo "IMAGE=$IMG"
echo "CREATED=$CREATED"
docker exec -u app "$C" sh -c "
  cd /app || exit 0
  if [ -f logs/LOOP_HOLD ]; then
    echo HOLD=HELD:\$(sed -n \"2p\" logs/LOOP_HOLD)
  else
    echo HOLD=released
  fi
  timeout 6 python3 scripts/ops/state-snapshot.py --app /app 2>/dev/null | grep -E \"^directive:|^opreq:\"
  echo COCKPIT=\$(curl -s -o /dev/null -w \"%{http_code}\" -m5 http://127.0.0.1:8787/api/status)
"
' 2>/dev/null)

field() { printf '%s\n' "$SSH_OUT" | grep -m1 "^$1=" | cut -d= -f2-; }
# state-snapshot.py'nin kendi satırları farklı biçimde: "anahtar: değer" (iki nokta,
# = değil) — field()'ın key=value varsayımına uymuyor, ayrı bir çekici gerekiyor.
rawline() { printf '%s\n' "$SSH_OUT" | grep -m1 "^$1:"; }

if [ -z "$SSH_OUT" ]; then
  echo "- **prod**: ULAŞILAMADI (Tailscale/ssh?) — konteyner durumu DOĞRULANMADI"
else
  CONTAINER=$(field CONTAINER)
  if [ "$CONTAINER" = "NONE" ] || [ -z "$CONTAINER" ]; then
    echo "- **prod**: konteyner BULUNAMADI (z12a992*)"
  else
    IMGSHA=$(field IMAGE | cut -d: -f2)
    CREATED=$(field CREATED)
    REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
    ORIGIN_MAIN=$(git -C "$REPO_ROOT" rev-parse origin/main 2>/dev/null)
    UNPUSHED=$(git -C "$REPO_ROOT" log --oneline origin/main..HEAD 2>/dev/null | wc -l | tr -d ' ')
    if [ -n "$IMGSHA" ] && [ -n "$ORIGIN_MAIN" ] && git -C "$REPO_ROOT" cat-file -e "$IMGSHA" 2>/dev/null; then
      IMG_VS_ORIGIN=$(git -C "$REPO_ROOT" log --oneline "${IMGSHA}..${ORIGIN_MAIN}" 2>/dev/null | wc -l | tr -d ' ')
      if [ "${IMG_VS_ORIGIN:-0}" -gt 0 ]; then
        DRIFT="⚠ image origin/main'in ${IMG_VS_ORIGIN} commit GERİSİNDE (taban ${IMGSHA:0:12}) — redeploy gerekir"
      elif [ "${UNPUSHED:-0}" -gt 0 ]; then
        DRIFT="image origin/main ile senkron, AMA sen origin/main'in ${UNPUSHED} commit ilerisindesin — PUSH edilmemiş"
      else
        DRIFT="image = origin/main = HEAD, tam senkron"
      fi
    else
      DRIFT="image tabanı doğrulanamadı (${IMGSHA:-?})"
    fi
    echo "- **prod**: $CONTAINER | oluşturuldu $CREATED | $DRIFT"
    echo "- **hold**: $(field HOLD)"
    echo "- **cockpit**: HTTP $(field COCKPIT)"
    echo "- **direktif**: $(rawline directive)"
    echo "- **oprq**: $(rawline opreq)"
  fi
fi

DEPLOY_DIR="$(cd "$(dirname "$0")/../../autocompany-deploy" 2>/dev/null && pwd)"
if [ -n "$DEPLOY_DIR" ] && [ -d "$DEPLOY_DIR/.git" ]; then
  SB=$(git -C "$DEPLOY_DIR" status -sb 2>/dev/null)
  BASLIK=$(printf '%s\n' "$SB" | head -1)
  KIRLI=$(printf '%s\n' "$SB" | tail -n +2 | grep -c .)
  DURUM="temiz"
  [ "${KIRLI:-0}" -gt 0 ] && DURUM="${KIRLI} dosya kirli"
  case "$BASLIK" in *"[ahead"*) DURUM="$DURUM, PUSH EDİLMEMİŞ commit var" ;; esac
  echo "- **autocompany-deploy**: $DURUM"
fi

PA="$(dirname "$0")/pending-actions.md"
if [ -f "$PA" ]; then
  OPEN=$(grep -cE "^- \[ \]" "$PA" 2>/dev/null)
  echo "- **bekleyen dış aksiyon**: ${OPEN:-0} (bkz. .claude/pending-actions.md)"
fi

# Prod-mekanizma tripwire kapsam senkronu: CLAUDE.md'nin kural bölümünde anılan
# her yüzeyi guard gerçekten koruyor mu? Temizken sessiz (brifing gürültü
# felsefesi); kayma varsa ⚠ satırı — kurala yüzey ekleyip script'i unutma
# hatasını her oturum başında yakalar.
GUARD="$(dirname "$0")/../scripts/prod-mechanism-guard.py"
if [ -f "$GUARD" ]; then
  SYNC_OUT=$(python3 "$GUARD" --check-sync 2>&1)
  if [ $? -ne 0 ]; then
    echo "- ⚠ **prod-guard kapsam kayması**: ${SYNC_OUT} — CLAUDE.md kuralı ile scripts/prod-mechanism-guard.py listesi aynı commit'te güncellenmeli"
  fi
fi

exit 0
