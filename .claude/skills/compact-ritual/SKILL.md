---
name: compact-ritual
description: Bağlam dolarken (gözcü %50/%60 uyarısı), kullanıcı compact öncesi hazırlık istediğinde, otomatik compact ertelendiğinde ya da compact/restart SONRASI toparlanırken uygula. Kararları repo adına özel resume dosyasına (/tmp/compact-<ad>-resume.md; tam yol: python3 scripts/compact_yol.py resume) şablonla kalıcılaştırır, lint'le doğrular VE compact SONRASI gerçek özetin (compact_summary) o kararları taşıyıp taşımadığını denetler; sayı taşınmaz — session-brief yeniden ölçer.
---

# compact-ritual — bağlam kaybını mekanikleştir

Ritüelin ölçülebilir HER parçası koda alındı; senin işin ölçülemeyeni taşımak:
kararlar, gerekçeler, doğrulanmamış çıkarımlar, tuzaklar.

## Neden bu biçimde

Elle yazılan resume metinleri iki şekilde zarar verir: (1) içindeki **sayılar**
bayatlar ve yanlış temelde karar aldırır, (2) ritüel "kullanıcı haber verir +
ajan hatırlar" varsayımına dayanır, oysa **otomatik compact haber vermez**.

Canlı kullanımda üç ek ders daha ödendi:

- İki compact üst üste geldi ve resume teslim edilemeden özet araya girdi —
  **kanonik resume DOSYADIR, sohbet mesajı kopyadır.** Dosya compact'ten
  etkilenmez; SessionStart brifingi onun gerçek yolunu ve yaşını gösterir,
  içeriği sen Read ile okursun.
- mtime'ı taze ama içeriği bozuk (eksik bölüm, sızmış sayı) resume'lar "taze"
  sayılıp sessizce geçti — **mekanik kapı, içerik doğrulamadan "tamam" diyemez**
  ("taze" = mtime <3sa VE lint yeşil).
- Hiçbir mekanizma compact SONRASI üretilen gerçek özetin (`compact_summary`)
  resume kararlarını fiilen taşıyıp taşımadığını görmüyordu — **compact SONRASI
  da iz bırakılmalı**, yalnız compact öncesi değil.

**Tek cümlelik kural: metin KARAR taşır, SAYI taşımaz.**

## Mekanizma haritası (ne otomatik, ne senin işin)

| Parça | Ne yapar |
|---|---|
| PreCompact → `compact-preflight.py` | Açık kalemleri `/tmp/compact-<ad>-preflight.md`'ye (tam yol: `python3 scripts/compact_yol.py preflight`) yazar. "Taze" = mtime <3sa VE `compact-resume-lint.py` yeşil. OTOMATİK compact'te taze değilse compact'i **bir kez** erteler (30 dk marker; manuel `/compact` asla bloklanmaz; kapatma: `COMPACT_AUTOBLOCK=0`). |
| PostCompact → `compact-postcheck.py` | Compact BİTTİKTEN SONRA çalışır, bloklayamaz. `compact_summary`'nin resume'un zorunlu bölüm başlıklarını (İLK İŞ/KARAR/…) içerip içermediğine bakar, `/tmp/compact-<ad>-history.log`'a (tam yol: `python3 scripts/compact_yol.py history`) JSON satır yazar. Bu bir KANARYADIR, kanıt değil — özetleyici paraphrase edebilir; amaç bir şey kaybolduğunda geriye dönük bakılabilecek bir iz. |
| SessionStart → `session-brief.py` | Sayıları YENİDEN ölçer; taze preflight ⚠'larını bağlama geri enjekte eder ve resume dosyasının GERÇEK yolunu + yaşını yazar. Resume İÇERİĞİNİ enjekte ETMEZ — compact sonrası o yolu Read ile oku. |
| UserPromptSubmit/PostToolUse → `context-watch.py` | %50 uyarı, %60 ritüel tetiği. |
| `compact-resume-lint.py` | Resume'da yasak sayı + eksik şablon bölümü avı — yabancı-okur testinin mekanik yarısı, VE preflight'ın "taze" kararının bir girdisi. |

Bu beşi SAYILARI ve SÜRECİ güvenceler; kararların içeriği hâlâ senden çıkar.
`tests/test_compact_ritual_hardening.sh` preflight'ın lint-gate'ini ve
postcheck'in ankor sayımını gerçek ritüel dosyalarına (resume, preflight, marker,
log) dokunmadan doğrular (`COMPACT_RESUME_PATH`/`COMPACT_PREFLIGHT_PATH`/
`COMPACT_BLOCK_MARKER`/`COMPACT_HISTORY_LOG` env override'ları).

**Yollar repo adına özeldir:** `/tmp/compact-<ad>-resume.md` (tam yol:
`python3 scripts/compact_yol.py resume`). `<ad>` repo adıdır; bağlı worktree'de
`-<worktree-dizini>` eklenir. Eski, ad taşımayan ortak `/tmp` yolları OKUNMAZ —
başka projenin resume'u olabilir.

## Compact ÖNCESİ adımlar

**1. Ön-kontrol:** `python3 scripts/compact-preflight.py` — her ⚠ için karar:
bitir, park et, ya da resume'a "İLK İŞ" yaz:
- *push edilmemiş commit* → push et
- *kaydedilmemiş değişiklik* → kimin işi, neden açık; silme
- *stash* → yarım iş mi, kasıtlı mı
- *projeye özel kontroller* (`.claude/preflight-extra.sh`) → aynı disiplin

**2. Resume'u DOSYAYA yaz:** şablon bu dizinde `resume-template.md` →
`/tmp/compact-<ad>-resume.md` (tam yol: `python3 scripts/compact_yol.py resume`;
Write aracıyla). Sohbete yapıştırmak 4. adımdır,
dosyaya yazmanın yerine GEÇMEZ — compact'i atlatan kopya dosyadır. Sayı yazma;
ölçüm gerekiyorsa ölçümün KOMUTUNU yaz ("şu an X" değil, "X'i şununla ölç").

**3. Lint:** `python3 scripts/compact-resume-lint.py` — kırmızıysa düzelt, tekrar
koş. Yeşil lint yabancı-okur testinin mekanik yarısıdır; insani yarısı sende:
okuyan biri doğrulanmamış bir şeyi "bitti" sanır mı, en tehlikeli tuzak işaretli
mi, durum ilk beş dakikada komutlarla doğrulanabilir mi?

**4. Tek mesaj:** kısa özet + resume metni + "compact'i sen başlatabilirsin".

## Compact/restart SONRASI adımlar

1. Brifingi oku — sayılar ORADAN. Brifingteki "resume dosyası" satırındaki yolu
   Read ile oku. Satır "YOK" diyorsa ya da dosya saatlerce eskiyse: özet metnine
   tek başına güvenme; preflight ⚠'ları + güncel ölçümden yeniden kur.
2. Arka plan izleyicilerini doğrula (aşağıdaki compact ≠ restart ayrımı);
   boş/eksikse güncel duruma göre YENİDEN kur — mükerrer kurma (önce süreç
   kontrolü).
3. Preflight ⚠ satırlarının hepsinin güncel karşılığını ölç; biri hâlâ açıksa
   İLK İŞ odur.

## İki farklı olay: compact ≠ restart

**Compact** (bağlam özetlemesi) aynı süreç içinde olur — `nohup`'lu OS süreçleri
VE oturuma bağlı arka plan bekleyicileri kesintisiz devam eder.

**Uygulama yeniden başlatması** farklıdır: alttaki oturum süreci TAMAMEN
sonlanır. `nohup`'lu OS süreçleri hayatta kalır; ama oturuma bağlı bekleyiciler
SESSİZCE ölür — bildirim asla gelmez, hata da vermez. Ayırt edemiyorsan görev
listesi kanıttır: "bildirim gelmedi" hiçbir zaman "iş bitti ya da hâlâ bekliyor"
anlamına gelmez.

## Sınırlar

- Ritüel iş bitirmez; kullanıcının kararı olan şeyi (bütçe, kapsam, zamanlama)
  resume'a SORU olarak taşı, kendiliğinden kapatma.
- Tazelik pencereleri sınırlıdır — brifingin taşıdığı satırları **doğrula**,
  körlemesine devralma.
- Otomatik erteleme EN FAZLA bir kez işler ve yalnız otomatik compact'te:
  "compact ertelendi" gerekçesi görürsen sebep resume'un yok/bayat/lint-kırmızı
  olmasıdır (gerekçe metni hangisi olduğunu söyler) — hemen 2-3. adımı koş; bir
  sonraki otomatik compact serbest geçer.
- Lint'i susturmak için sayıyı gizleme (yazıyla yazmak dahil) — sayı gerekiyorsa
  o bir ÖLÇÜMDÜR ve yeri resume değil, brifingin komutlarıdır.
- `compact-postcheck.py`'nin kanarya uyarısı bir SONUÇ değil bir İPUCUDUR:
  ankor eşleşmesi tam-dize aranır, özetleyici paraphrase ederse yanlış-pozitif
  üretebilir. Uyarı görürsen `/tmp/compact-<ad>-history.log`'a
  (tam yol: `python3 scripts/compact_yol.py history`) bak ama panikleme;
  asıl kanıt her zaman canlı ölçümdür.
- **Sabit bağlam tabanı ritüelin kapsamı DIŞINDA:** her turda yeniden enjekte
  edilen şeyler (skill gövdeleri, CLAUDE.md, hafıza, araç listeleri) compact'le
  SIFIRLANMAZ — compact biter bitmez doluluk yeniden eşiğe yaklaşabilir. Ritüel
  konuşma GEÇMİŞİNİ kısaltır, bu sabit tabanı değil. Kontrol edilebilir tek
  kaldıraç: sık-enjekte-edilen skill gövdelerini kısa ve yalnız-gerekli tutmak
  (progressive disclosure — detay ayrı dosyaya, SKILL.md'ye değil). Bu tabanı
  sıfıra indirmeye çalışmak zaman kaybıdır; kabul edilmiş bir maliyettir.
