# scripts/ops/rfq-send.py · [[outreach-eligibility-sending]] [[rfq-send]]

Anonim OPEX RFQ göndericisi — §15 Sponsor İzni kapısı, günlük/toplam cap'ler ve ForwardEmail teslimi ile fail-closed çalışan, tender send-gate'in RFQ kardeşi.

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
- render · function · L155-L163 — Şablon adından scope'u çözüp vendor kümesi için subject/plain-text/HTML içeriği üretir.
- anonymity_scan · function · L166-L171 — Render edilen metinde denylist (wowcar) sızıntısı olup olmadığını arar.
- decide · function · L174-L197 — Bir vendor kaydını opt-out, never-twice, e-posta varlığı, anonimlik, cap'ler ve §15 izni sırasıyla değerlendirip ALLOW/REFUSE kararı döndürür.
- _encode_subject · function · L201-L204 — Konuyu RFC 2047 base64 encoded-word'e çevirerek Türkçe karakter bozulmasını önler.
- send_fe · function · L207-L225 — ForwardEmail /v1/emails'e Basic auth ile form-encoded e-posta gönderir ve yanıtı döndürür.
- _mark_sent · function · L228-L231 — Gönderim sonrası kaydı 'Gönderildi' ve zaman damgası ile PATCH'ler.
- main · function · L235-L277 — CLI girişi: --report ile cap/eligibility özeti, --record ile tek vendor kararı ve --send ile gerçek gönderim sonrası kaydı işaretler.
