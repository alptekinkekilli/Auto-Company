# Bekleyen dış aksiyonlar (insan/karşı taraf bekleyen işler)

Biçim önemli: `- [ ]` satırları preflight'ta ⚠ (açık kalem) sayılır; biten işi `- [x]` yap.
Her kalemde SAHİBİ ve varsa mutlak tarih olsun.

- [x] **Prod redeploy** — KAPANDI 2026-08-06T14:46Z. Kök neden: `main`'in tracking'i
      ilgisiz bir fork'a bağlıydı, `origin`'e hiç push gitmiyordu (`git status` bunu
      hiç göstermedi). Push edildi + tracking düzeltildi, sonra Coolify API'den GERÇEK
      redeploy tetiklendi (`/api/v1/deploy`, hot-patch değil). Yeni konteyner
      `z12a992i3ty202zezspij2fn-144411171194`, image `ea3b394` (= o anki HEAD),
      `[LOOP-HOLD]` ile güvenli açıldı (persistent volume'daki hold'u devraldı, sıfır
      model çağrısı), 30/30 test geçti. Konteyner şu an HELD, RELEASE operatörden.
- [ ] **Konteynerin 2026-08-06T13:00:01'de neden yeniden yaratıldığı** hâlâ tam
      açıklanamadı. Kesinleşen: gerçek bir Coolify build+deploy'du (image 12:59:00'da
      taze build edilmiş, `journalctl -u ssh`'te Coolify Cloud IP'sinden 12:57-13:01
      arası yoğun SSH oturum patlaması var — Coolify Cloud'un deploy IP'si diğer
      günlerde de tekli "ping" oturumlarıyla görünüyor, o burst farklı). Ama bir PUSH'a
      tepki DEĞİLDİ — o güne kadarki son push 08-04'teydi, 4 saat önce değil 2 gün önce.
      Zamanlanmış bir Coolify işi mi, panelden manuel bir tık mı ayırt edilemedi (Coolify
      API'sinde deployment audit-log endpoint'i bulunamadı). Sahibi: operatör (Coolify
      panelinden kim/ne tetikledi kontrol edebilir) veya ben, sonraki oturum.
- [ ] **GitHub repo `alptekinkekilli/Auto-Company` PUBLIC** (`gh api .../--jq .private`
      → `false`, 2026-08-06 tespit). Git geçmişinde hızlı sır taraması yapıldı, gerçek
      bir sızıntı bulunmadı (3 eşleşme hepsi placeholder: AWS'in kendi örnek anahtarı,
      Slack'in örnek `xoxb-12345`, ve `CLAUDE_CODE_OAUTH_TOKEN` bir değişken adı olarak)
      — ama bu tam bir tarama değil. Hafızadaki iki bekleyen token sızıntısı (08-01 ps
      leak, 08-03 transcript leak, ikisi de "beklesin" kararıyla rotasyonsuz) repo public
      olduğu için daha riskli olabilir. Sahibi: operatör — private'a almak mı, yoksa
      bilerek mi public tutuluyor, karar operatörün.
