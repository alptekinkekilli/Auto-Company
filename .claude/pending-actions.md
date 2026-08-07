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
- [x] **GitHub repo `alptekinkekilli/Auto-Company` PUBLIC — TAM tarama yapıldı** (gitleaks
      8.30.1, 2026-08-07: working-tree 17 eşleşme + 763 commit'lik git-history taraması 6
      eşleşme). Önceki "hızlı regex, gerçek sızıntı yok" değerlendirmesi YANLIŞTI —
      gitleaks gerçek bir bulgu çıkardı:
      - **GERÇEK, CANLI, HÂLÂ AÇIK sızıntı: 3 adet SnapOG `msk_...` API anahtarı**
        (`docs/qa/evidence/snapog/register-{free,pro,business}-response.html`) — kendi
        SnapOG ürünümüzün backend'inin QA test kayıtlarına gerçekten bastığı anahtarlar,
        placeholder değil. Repo'yu private yapmak bunu GERİYE DÖNÜK silmez (zaten public
        geçirdiği süre boyunca taranmış/indekslenmiş olabilir) — **rotasyon/iptal, görünürlük
        kararından BAĞIMSIZ ve daha öncelikli bir aksiyon**. Sahibi: operatör veya ben
        (SnapOG backend'ine nasıl erişileceği belli olursa).
      - Geri kalan 17-6 eşleşmenin hepsi doğrulanan yanlış pozitif: `claimToken=...` bir
        Cloudflare claim linki ama 2026-07-21'de 60 dakikalık pencereyle sınırlıydı, çoktan
        süresi doldu; `bridge_leak_scan.py`'daki "sızıntı" kendi test fixture'ı (dosyanın
        kendi docstring'i bunu doğruluyor); `security-audit` skill'indeki jwt-secret
        dokümantasyon örneği (`c3VwZXJzZWNyZXQ=` = base64 "supersecret"); wrangler KV
        namespace-id bir kimlik, sır değil; `ANTHROPIC_API_KEY=` bir değişken ADI, değer
        değil.
      - Repo private/public kararı hâlâ operatörün — ama artık gerçek bulgularla: SnapOG
        anahtarları rotasyon gerektiriyor GÖRÜNÜRLÜKTEN BAĞIMSIZ; hafızadaki iki eski
        token sızıntısı (08-01 ps leak, 08-03 transcript leak) hâlâ rotasyonsuz duruyor.
