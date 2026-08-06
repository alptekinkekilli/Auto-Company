# Bekleyen dış aksiyonlar (insan/karşı taraf bekleyen işler)

Biçim önemli: `- [ ]` satırları preflight'ta ⚠ (açık kalem) sayılır; biten işi `- [x]` yap.
Her kalemde SAHİBİ ve varsa mutlak tarih olsun.

- [ ] **Prod redeploy gerekiyor** (2026-08-06T17:16Z tespit edildi). Konteyner
      2026-08-06T13:00:01Z'de `origin/main`'in o anki ucu olan `440875a`'dan yeniden
      yaratıldı — aynı gün `docker exec`+tar ile yapılan 6 commit'lik canlı yama
      (IDLE-SKIP, kill-switch canlı-okuma düzeltmesi, cockpit bildirimi, tool-usage
      --names, üç-kusur düzeltmesi) konteynerin yazılabilir katmanıyla birlikte gitti.
      Kök neden BULUNDU ve KAPATILDI: `main`'in upstream tracking'i yanlışlıkla ilgisiz
      bir fork'a (`upstream/main`) bağlıydı, gerçek repo (`origin`) hiç push
      görmüyordu — 2026-08-06T17:2xZ'de `git push origin main` yapıldı ve tracking
      `origin/main`'e düzeltildi; `origin/main` şu an `2f777e1` ile birebir. Kalan
      tek iş: konteyneri bu güncel image'den redeploy etmek (Coolify) veya
      hold->sync->restart->release ritüeliyle tekrar canlı yamayı uygulamak. Sahibi:
      operatör Hold'a basınca ben tamamlarım.
- [ ] **Konteynerin neden 13:00:01'de yeniden yaratıldığı araştırılmadı** — Coolify
      auto-redeploy mi, restart policy mi, health-check mi, manuel bir tetik mi
      bilinmiyor. "Deploy yalnız hold altında" değişmezi bir yerde delinmiş olabilir.
      Sahibi: operatör veya ben, sonraki oturum.
