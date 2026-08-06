---
name: compact-ritual
description: Compact öncesi sertleştirilmiş ritüel — ön-kontrolü koş, açık kalemleri kapat, kararları (sayıları DEĞİL) taşıyan resume'u üret, yabancı-okur testinden geçir. Kullanıcı "compact yapacağım" dediğinde, /compact-ritual çağrıldığında ya da bağlam doluluğu eşiği aşıldığında (context-watch hook'u haber verir).
---

# compact-ritual — bağlam kaybını mekanikleştir

Ritüelin ÖLÇÜLEBİLİR kısmı koda alındı; senin işin ölçülemeyeni taşımak.

## Neden bu biçimde

Elle yazılan resume metinleri iki şekilde zarar verir: (1) içindeki **sayılar**
bayatlar ve yanlış temelde karar aldırır, (2) ritüel "kullanıcı haber verir + ajan
hatırlar" varsayımına dayanır, oysa **otomatik compact haber vermez**. Bu yüzden
ön-kontrol `PreCompact` hook'undan (manual VE auto) kendiliğinden koşar; sayılar
compact sonrası `session-brief.py` ile yeniden ölçülür.

**Tek cümlelik kural: metin KARAR taşır, SAYI taşımaz.**

## Adımlar

**1. Ön-kontrolü koş, ⚠ satırlarını KAPAT.**

```bash
python3 scripts/compact-preflight.py
```

Her ⚠ için karar: bitir, park et, ya da resume'a "İLK İŞ" olarak yaz.
- push edilmemiş commit → push et
- kaydedilmemiş değişiklik → kimin işi, neden açık; silme
- stash → yarım iş mi, kasıtlı mı
- projeye özel kontroller (`.claude/preflight-extra.sh`) → aynı disiplin

**2. Sayı taşıma, komut taşı.** HEAD, süre, maliyet, kuyruk uzunluğu, süreç sayısı
resume'a YAZILMAZ; compact sonrası brifing bunları yeniden ölçer.

**3. Resume metnini üret — yalnız yeniden üretilemeyenler:**
- kullanıcının bu oturumdaki KARARLARI ve gerekçeleri (birebir, yorumsuz)
- yürürlükteki kısıtlar, yetki sınırları
- bekleyen soru / kullanıcıdan beklenen cevap
- kurulu arka plan izleyicileri ve ne bekledikleri (yeniden kurmadan ÖNCE süreç kontrolü)
- doğrulanmış olgu ile doğrulanmamış çıkarımın AYRIMI

**4. Yabancı-okur testi.** Bu metni okuyan biri: (a) ilk beş dakikada durumu
doğrulayabiliyor mu, (b) doğrulanmamış bir şeyi "bitti" sanır mı, (c) en tehlikeli
tuzak işaretli mi? Üçü de geçmiyorsa düzelt.

**5. Tek mesaj:** kısa özet + tek kod bloğunda resume. Compact'i kullanıcı başlatır.

## Sınırlar

- Ritüel iş bitirmez. Kullanıcının kararı olan şeyi (bütçe, kapsam, zamanlama)
  kendiliğinden kapatma — resume'a soru olarak taşı.
- `/tmp/compact-preflight.md` satırlarını **doğrula**, körlemesine devralma.
