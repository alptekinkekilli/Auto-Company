# scripts/ops/rfq-send.py · [[fail-closed-gating-invariant]] [[never-twice-dedup-invariant]] [[rfq-send]] [[rfq-send-pipeline]] [[secret-handling]]

Anonim OPEX RFQ göndericisi: §15 sponsor izni gated, fail-closed, ForwardEmail üzerinden e-postalı vendor'lara indikatif fiyat talebi gönderir.

- _load_key · function · L90-L111 — API anahtarını env → runtime.env → macOS Keychain sırasıyla yükler ve env'e yazar.
- _app_dir · function · L114-L116 — Script'in iki üst dizinini (repo kökü) mutlak yol olarak döndürür.
- _air · function · L120-L132 — Airtable REST isteğini (GET/PATCH) yürütüp JSON yanıtını döndüren genel yardımcı.
- _record · function · L135-L136 — Tek bir Airtable kaydını ID ile çeker.
- _all_rows · function · L139-L150 — Tablodaki tüm kayıtları offset sayfalama ile toplar.
- _sponsor_ok · function · L154-L155 — §15 kapısı: 'Sponsor İzni' checkbox'ı tam olarak True ise izin verir, aksi halde fail-closed reddeder.
- _opted_out · function · L158-L159 — Vendor'ın opt-out bayrağının set edilip edilmediğini döndürür.
- _already_sent · function · L162-L163 — Kaydın daha önce gönderilip gönderilmediğini (Durum veya Gönderim TS) kontrol eder.
- _email_of · function · L166-L168 — Kanal alanından ilk e-posta adresini regex ile çıkarır, yoksa None.
- _caps_now · function · L171-L181 — Bugünkü ve toplam gönderim sayısını UTC tarihine göre hesaplar.
- render · function · L184-L191 — Şablon adından kapsam metnini seçip konu ve anonim gövde metnini üretir.
- anonymity_scan · function · L194-L199 — Render edilen metinde denylist (wowcar) sızıntısı olup olmadığını arar.
- decide · function · L202-L224 — Tüm gate'leri (opt-out, never-twice, e-posta, render, anonimlik, cap'ler, §15) sırayla değerlendirip ALLOW/REFUSE kararı üretir.
- _encode_subject · function · L228-L231 — Konuyu RFC 2047 base64 encoded-word'e çevirerek Türkçe karakter bozulmasını önler.
- send_fe · function · L234-L249 — ForwardEmail /v1/emails'e Basic auth ile form-encoded e-posta gönderir ve yanıtı döndürür.
- _mark_sent · function · L252-L255 — Gönderim sonrası kaydı 'Gönderildi' ve zaman damgası ile PATCH'ler.
- main · function · L259-L301 — CLI: --report ile cap/eligibility özeti, --record ile dry-run veya --send ile gerçek gönderim ve başarıda kaydı işaretler.
