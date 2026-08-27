# scripts/ops/rfq-send.py · [[opex-rfq-send-gate]] [[rfq-send]]

CLI that sends anonymous OPEX RFQ emails to vendors via ForwardEmail, gated by a §15 operator consent checkbox and daily/total caps, fail-closed.

- _load_key · function · L61-L82 — API anahtarını env → runtime.env → macOS Keychain sırasıyla yükler ve env'e yazar.
- _app_dir · function · L85-L87 — Script'in iki üst dizinini (repo kökü) mutlak yol olarak döndürür.
- _air · function · L91-L103 — Airtable REST isteğini (GET/PATCH) yürütüp JSON yanıtını döndüren genel yardımcı.
- _record · function · L106-L107 — Tek bir Airtable kaydını ID ile çeker.
- _all_rows · function · L110-L121 — Tablodaki tüm kayıtları offset sayfalama ile toplar.
- _sponsor_ok · function · L125-L126 — §15 kapısı: 'Sponsor İzni' checkbox'ı tam olarak True ise izin verir, aksi halde fail-closed reddeder.
- _opted_out · function · L129-L130 — Vendor'ın opt-out bayrağının set edilip edilmediğini döndürür.
- _already_sent · function · L133-L134 — Kaydın daha önce gönderilip gönderilmediğini (Durum veya Gönderim TS) kontrol eder.
- _email_of · function · L137-L139 — Kanal alanından ilk e-posta adresini regex ile çıkarır, yoksa None.
- _caps_now · function · L142-L152 — Bugünkü ve toplam gönderim sayısını UTC tarihine göre hesaplar.
- render · function · L155-L161 — Builds the RFQ subject and body from the record's template and cluster using the shared rfq_template module.
- anonymity_scan · function · L164-L169 — Render edilen metinde denylist (wowcar) sızıntısı olup olmadığını arar.
- decide · function · L172-L194 — Tüm gate'leri (opt-out, never-twice, e-posta, render, anonimlik, cap'ler, §15) sırayla değerlendirip ALLOW/REFUSE kararı üretir.
- _encode_subject · function · L198-L201 — Konuyu RFC 2047 base64 encoded-word'e çevirerek Türkçe karakter bozulmasını önler.
- send_fe · function · L204-L219 — ForwardEmail /v1/emails'e Basic auth ile form-encoded e-posta gönderir ve yanıtı döndürür.
- _mark_sent · function · L222-L225 — Gönderim sonrası kaydı 'Gönderildi' ve zaman damgası ile PATCH'ler.
- main · function · L229-L271 — CLI: --report ile cap/eligibility özeti, --record ile dry-run veya --send ile gerçek gönderim ve başarıda kaydı işaretler.
