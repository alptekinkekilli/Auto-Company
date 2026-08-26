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
- [x] **Konteynerin 2026-08-06T13:00:01'de neden yeniden yaratıldığı** — KAPANDI
      2026-08-07, operatörün Coolify panelinden yapıştırdığı deploy kaydıyla: Success,
      12:57:26→13:00:33 UTC (SSH-burst penceremle birebir örtüşüyor), commit `440875a`.
      O commit'in gerçek push zamanı (GitHub API'den doğrulandı): 2026-08-04T18:00:36Z —
      deploy'dan TAM 2 GÜN ÖNCE. Yani gerçek, panelde görünen, başarılı bir deploy, ama
      push'a tepki değil (kim/ne panelden tetikledi önemsiz kaldı — mekanizma sıradan,
      rogue değil).
- [x] **GitHub repo `alptekinkekilli/Auto-Company` PUBLIC — TAM tarama yapıldı, operatör
      kararı: public kalsın.** KENDİ METODOLOJİ HATAM burada bir kez yanlış "canlı sızıntı"
      alarmı üretti — düzeltiliyor. `gitleaks detect --no-git` çalıştırdım: bu mod DİSK
      ÜZERİNDEKİ dosyaları tarar, `.gitignore`'a BAKMAZ. 17 eşleşme buldu, ben bunları
      "3 canlı SnapOG API anahtarı public'te" diye raporladım ve operatörü buna göre
      karar verdirttim (rotasyon onayı ald ım) — YANLIŞTI. Doğrulama: `git ls-files` /
      `git cat-file -e origin/main:<path>` ile tek tek kontrol edince, o 17 eşleşmenin
      TAMAMI ya `docs/*`, `logs/*`, `memories/*`, `__pycache__` (hepsi `.gitignore`'da,
      hiçbiri `origin/main`'de yok — SnapOG `msk_` anahtarları dahil, hepsi yerel-diskte-
      kalan QA kanıtı, PUSH EDİLMEMİŞ) ya da zaten tekrar eden aynı 6 dosyaydı. D1'e
      "rotasyon" için attığım SELECT sorgusu da bunu doğruladı: o 3 key_hash prod DB'de
      HİÇ yok (zaten hiç prod'a gitmemiş, muhtemelen `wrangler dev` yerel testinden).
      **Hiçbir UPDATE/DELETE çalıştırılmadı, gerçek zarar yok — ama operatöre yanlış
      "canlı sızıntı, rotasyon gerekiyor" bilgisiyle karar aldırdım, bu hatalıydı.**
      Doğru/güvenilir ölçüm — git-history modu (`gitleaks detect --log-opts="--all"`,
      `.gitignore`'a saygılı, sadece GERÇEKTEN push edilmiş 763 commit'i tarar) —
      6 eşleşme buldu, hepsi doğrulanmış yanlış pozitif: `bridge_leak_scan.py`'nin kendi
      test fixture'ı (docstring bunu doğruluyor), `security-audit` skill'inin jwt-secret
      dokümantasyon örneği (`c3VwZXJzZWNyZXQ=`=base64"supersecret"), wrangler KV
      namespace-id (kimlik, sır değil), `ANTHROPIC_API_KEY=` bir değişken ADI (değer yok).
      **Sonuç: public repo'da gerçek sızıntı YOK — orijinal "hızlı regex" değerlendirmesi
      doğruymuş, ben yanlışlıkla "yanlıştı" dedim.** Hafızadaki iki eski token sızıntısı
      (08-01 ps leak, 08-03 transcript leak) konusu bu bulgudan etkilenmiyor, ayrı durur.

- [x] **Router floor 168h — redeploy-sonrası fiili teyit** — KAPANDI 2026-08-26: ara redeploy'lar sonrası loop process (pid 172) environ'ında `ROUTER_DIRECTIVE_MIN_HOURS=168` doğrulandı (canlı). Orijinal not: — SAHİP: sonraki doğal redeploy
      (container hash ≠ `-152423747967`). `ROUTER_DIRECTIVE_MIN_HOURS=168` runtime.env'de
      staged; boot'ta canlı olacak (entrypoint export). Deterministik kanıt ZATEN var
      (boot-sim: floor 168 → PENDING directive düşüyor, router "silent"). Redeploy olunca
      TEYİT ET: yeni container'da `ROUTER_DIRECTIVE_MIN_HOURS` loop env'de = 168 VE
      `operator-action-router.py --app /app --dry-run` → "no open operator items — silent"
      (directive <168h iken). Sonra APP-302 checklist kalemini tickle. Zorlama redeploy YOK
      (operatör "doğal uygula"). Ref: [[operator-action-router]] memory + consensus stamp
      2026-08-26 #2.
