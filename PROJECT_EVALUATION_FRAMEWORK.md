# Proje Değerlendirme ve Yönlendirme Çerçevesi

Bu belge, yeni veya mevcut bir ürün fikrini değerlendirirken kullanılacak standart karar formatıdır. Amaç yalnızca fikir hakkında yorum yapmak değil; pazar gerçeği, müşteri ihtiyacı, rekabet, dağıtım, ürün yeterliliği ve doğrulama verilerini birlikte değerlendirerek uygulanabilir bir yönlendirme üretmektir.

Her proje için mümkün olduğunda güncel ve birincil kaynaklarla araştırma yapılır. Güvenilir veri bulunmayan alanlarda oran veya pazar büyüklüğü uydurulmaz; bilinmeyenler açıkça belirtilir ve bunları ölçmek için deney tasarlanır.

## Temel karar ilkeleri

1. Çalışan kod, doğrulanmış iş modeli anlamına gelmez.
2. İlgi, trafik, kayıt ve ücretsiz kullanım tek başına ödeme isteğini kanıtlamaz.
3. Bir regülasyonun varlığı, bağımsız bir yazılım ürününe otomatik olarak talep yaratmaz.
4. En önemli rakip her zaman başka bir startup değildir; ücretsiz araçlar, açık kaynak, platformun yerleşik özelliği, manuel çözüm ve hiçbir şey yapmamak da rakiptir.
5. Ürün özelliği ile müşterinin satın aldığı sonuç birbirinden ayrılmalıdır.
6. Pazar boşluğu olduğu varsayılmamalı; doğrudan ve dolaylı alternatifler araştırılmalıdır.
7. Yeni özellik geliştirmeden önce ödeme isteği mümkün olan en ucuz yöntemle test edilmelidir.
8. Yaklaşan son tarih veya trend, zayıf talebi gizlemek için gerekçe olarak kullanılmamalıdır.
9. Hukuki, finansal veya güvenlik iddiaları garanti gibi pazarlanmamalıdır.
10. Her öneri ölçülebilir devam, pivot ve durdurma eşiklerine bağlanmalıdır.
11. Yalnızca yeni önerilen eksenlerde `PROMPT.md → SEARCH REGIME` politikasını uygula. Bu politika Selected/Pending adayları geriye dönük değerlendirmez; madde 4 ve bölüm 5'teki ikame analizini, WTP HARD STOP'u veya mevcut yetki sınırlarını değiştirmez.

## İnceleme için gerekli girdiler

Mevcut olanlar paylaşılır; eksik bilgiler araştırılır veya varsayım olarak açıkça işaretlenir:

- Ürün veya repo bağlantısı
- README, karar belgesi veya ürün özeti
- Hedef müşteri
- Çözülen problem
- Mevcut fiyat veya gelir modeli
- Ürünün mevcut aşaması
- Kullanıcı, görüşme, satış ve dönüşüm verileri
- Rakipler ve müşterinin mevcut çözüm şekli
- Dağıtım planı
- Varsa regülasyon veya son tarih iddiası
- Ekibin vermeye çalıştığı karar

## Fırsat kaydı ve tarama dedup (ZORUNLU — önce bunu oku)

Herhangi bir fırsat taraması (opportunity scan) veya beyin fırtınasından **önce**
`memories/candidate-registry.md` yüklenir. Bu kayıt üç liste tutar:

- **Selected Candidates** — operatörün seçtiği, üzerinde çalışılan projeler.
- **Archived Candidates** — öldürülen / NO-GO / durdurulan fikirler.
- **Pending Queue** — önerilmiş ama operatör kararı bekleyen adaylar.

Dedup anahtarı **isim değil, eksen (axis) = (alıcı × teslim biçimi × fiyat noktası)**'dır —
yeniden paketlenmiş ama aynı eksendeki bir fikir de tekrardır. Yeni bir fırsat önerirken:

- **Selected** ile aynı eksen → zaten yürütülüyor, yeni diye önerme.
- **Archived** ile aynı eksen → KAPSAM DIŞI, diriltme; hangi kayıt ve neden öldürüldüğünü belirt.
- **Pending Queue** ile aynı eksen → zaten önerilmiş, yeniden üretme.
- Yalnızca **temsil edilmemiş** bir eksende fırsat sun. Neyi elediğini ve nedenini **logla** —
  sessizce atlama yok.

Kayıt her döngü güncellenir: operatör bir adayı seçince Selected'e (Linear issue ile);
bir aday öldürülünce Archived'e (karar + tek satır gerekçe) taşınır. **Arşiv kaydı asla
sessizce silinmez** — re-proposal döngüsünün sebebi tam olarak budur. Bu kapı yalnızca neyin
önerileceğini yönetir; hiçbir zaman bir build yetkisi vermez (WTP HARD STOP hâlâ geçerlidir).

## İhale (tender) adayları için zorunlu ön-kontrol (ZORUNLU — herhangi bir efor harcanmadan önce)

**Neden var:** `208-A` Konak `2026/0003` adayında iki bağımsız iş modeli-öncesi
hata bulundu — ihalenin teklif tarihi (`11.06.2026 11:00`) analiz tarihinde
(`2026-07-25`) zaten 44 gün geçmişti, hiçbir cycle bunu kontrol etmedi/fark
etmedi. Operatör bunu kendisi, otorite sayfasını okuyarak buldu. Bu bölüm bu
kontrolü elle istenen bir şey olmaktan çıkarıp **standart, atlanamaz bir kabul
adımı** hâline getirir.

Herhangi bir ihale adayı için requirement-to-evidence matrisi, cost-driver
register veya başka bir detaylı analiz **başlamadan önce**, çıktının ilk iki
maddesi olarak açıkça doğrulanır ve yazılır:

1. **Teklif/son tarih hâlâ gelecekte mi?** Bugünün tarihini ve ihalenin
   beyan edilen teklif tarih/saatini yan yana yaz, karşılaştır. Geçmişse
   `INPUT FAIL` ile hemen dur — daha ileri efor harcama, bu doğru davranıştır,
   eksik tamamlama değil.
2. **Kategori/kapsam mantıklı ve şirketin manuel/no-code bir iç fizibilite
   paketiyle sınırlandırabileceği bir hizmet türü mü?** Kategori kendisi artık
   otomatik bir eleme sebebi DEĞİL (operatör kararı, 2026-07-27) — şirket
   herhangi bir yasal, kamuya açık ihale kategorisini değerlendirebilir. Ama
   yine de aday, `PROMPT.md → BOUNDED INTERNAL FEASIBILITY PACKETS`'ın mevcut
   yetki sınırları içinde kalmalı: manuel/no-code inceleme, satın alma yok,
   dış iletişim yok, bid submission yok.

Bu iki kontrol geçmeden hiçbir tam paket (requirement matrisi, cost-driver
register, contribution senaryoları) üretilmez. Erken ve doğru bir dur, paketi
tamamlayamamaktan daha iyi bir sonuçtur — bkz.
`docs/ceo/cycle272-208a-konak-disqualification-result.md`.

## İhale belge işleme — kurumsal know-how (Cycle 274)

`208-A`'nın Konak paketi üzerinde çalışılırken öğrenilenler, tek seferlik bir
cycle çıktısı olarak kaybolmasın diye burada kalıcı hale getirildi.

**Kullanılabilir belirlenimci araçlar (container'da hazır, LLM çağrısı
gerektirmez):** `.docx`/`.xlsx` metin ve tablo çıkarımı için `python3-docx` /
`python3-openpyxl` / `python3-pandas`; eski `.doc`/`.xls` formatlarını modern
formata çevirmek için `soffice --headless --convert-to <format>`
(LibreOffice); `.pdf` metin çıkarımı için `pdftotext` (poppler-utils —
Cycle 276'da eksik olduğu görülüp eklendi, çoğu ihalenin idari/teknik
şartnamesi PDF'tir); taranmış/gömülü görsel içerik için `tesseract -l tur`
OCR (Türkçe dil paketi dahil). **Not:** bazı "PDF" belgeler aslında taranmış
görüntüdür (`pdftotext` anlamsız/bozuk karakterler döner — bu durumda önce
`pdffonts`/`pdfimages -list` ile kontrol et; gerçek metin yoksa `pdftoppm` ile
sayfaları görsele çevirip `tesseract -l tur` ile OCR yap). Cycle 276/277'de
PTT'nin Teknik Şartname.pdf'i tam olarak bu durumdaydı.

**Türk kamu ihalelerinde tipik olarak görülen belge sınıfları** (otorite
sayfasında doğrudan bağlantılı, genelde ücretsiz — ayrı bir "tam paket" ücretli
satın alma yalnızca ek belgeler/zeyilname geçmişi için gerekebilir):

- Teknik Şartname, İdari Şartname, Sözleşme Taslağı (ana üç belge)
- Ekler: Geçici Teminat Mektubu, Kesin Teminat Mektubu, Banka Referans
  Mektubu, Bilanço Bilgileri Tablosu, Yasaklı Olmadığına Dair Taahhütname,
  Açık Maliyet Analizi, Birim Fiyat Teklif Cetveli, Birim Fiyat Teklif
  Mektubu, Evrak Listesi, İş Deneyim Belgesi

**En kritik metodolojik ders:** bu belgelerin çoğu **boş şablondur** —
otorite tarafından yayınlanan, teklif sahibinin dolduracağı formlar. "Belge
mekanik olarak okunabilir" ile "teklif sahibinin dosyası eksiksiz ve
doldurulmuş" birbirinden kesinlikle ayrılmalıdır. Boş bir maliyet
hücresi/formülü **asla sıfır maliyet olarak yorumlanmaz** — `UNKNOWN` olarak
işaretlenir. Mali, hukuki, vergi, sigorta ve lisans/uygunluk yargıları asla
tahmin edilmez; `SPECIALIST REFERRAL` olarak dışarı yönlendirilir.

**Standart çıktı biçimi:** requirement-to-evidence matrisi
(`MET` / `GAP` / `AMBIGUOUS` / `SPECIALIST REFERRAL`), her satırda kaynak
dosya + paragraf/tablo/hücre referansı ile — bkz.
`docs/ceo/cycle274-208a-konak-document-tools-infrastructure-test.md` referans
uygulama olarak. Bu format artık herhangi bir gelecekteki ihale fizibilite
paketi için standart şablondur, tekrar icat edilmesine gerek yok.

## Standart değerlendirme süreci

### 1. Ürünü sade biçimde tanımla

- Ürün gerçekte ne yapıyor?
- Müşteri hangi sonucu satın alıyor?
- Ücretli olan şey özellik mi, sonuç mu, güven mi, zaman tasarrufu mu?
- Ürünün iddiası ile mevcut uygulaması birbirini karşılıyor mu?

### 2. Problemi değerlendir

- Problem gerçek mi?
- Ne sıklıkla yaşanıyor?
- Acil mi, ertelenebilir mi?
- Müşteri bugün bu problemi nasıl çözüyor?
- Çözülmemesinin somut maliyeti nedir?
- Kullanıcı ile ödeme yapan kişi aynı mı?

### 3. Pazarı araştır

- Hedef müşteri grubu ne kadar geniş?
- Ürünün kapsadığı gerçek alt segment hangisi?
- Güvenilir kullanım veya penetrasyon verisi var mı?
- Pazar yeni mi, büyüyen mi, doygun mu?
- Talep davranışla mı, yalnızca haber ve trendlerle mi destekleniyor?
- Bilinmeyen pazar verisi hangi deneyle ölçülebilir?

### 4. Alternatifleri ve rekabeti incele

Rakipler beş grupta ele alınır:

1. Doğrudan ücretli rakipler
2. Ücretsiz ve açık kaynak araçlar
3. Platforma gömülü özellikler
4. Manuel veya hizmet tabanlı çözümler
5. Hiçbir şey yapmama seçeneği

Her alternatif için şu sorular cevaplanır:

- Aynı ihtiyacın ne kadarını karşılıyor?
- Fiyatı ve dağıtım avantajı nedir?
- Müşterinin geçiş yapmasını gerektiriyor mu?
- Bizim giriş noktamızı ücretsiz biçimde kapatıyor mu?
- Rakibin kolayca ekleyebileceği bir özellik mi geliştiriyoruz?

### 5. Ürün yeterliliğini kontrol et

- Ürün vaat ettiği sonucu uçtan uca sağlıyor mu?
- Kritik işlem gerçekten gerçekleşiyor mu, yoksa yalnızca arayüzde gösteriliyor mu?
- Entegrasyon, erişilebilirlik, güvenlik ve ölçüm eksikleri var mı?
- Kullanıcının yanlış güven duymasına yol açabilecek iddialar var mı?
- Teknik olarak hazır olmakla ticari olarak hazır olmak ayrılmış mı?

### 6. Gelir modelini değerlendir

- Müşteri neden para öder?
- Tek seferlik satış mı, tekrar eden değer mi?
- Ürün kolay kopyalanabilir mi?
- Sürekli gelir için gerçek bir sürekli hizmet var mı?
- Fiyat müşterinin alternatif maliyetleriyle uyumlu mu?
- En iyi alıcı son kullanıcı mı, ajans mı, platform mu, kurum mu?

### 7. Dağıtım avantajını değerlendir

- İlk 50 nitelikli müşteriye nasıl ulaşılacak?
- Ürünün organik, viral, ortaklık veya platform dağıtımı var mı?
- Rakip müşteriye bizden önce hangi kanaldan ulaşıyor?
- Satış mesajı genel korkuya mı, gözlemlenmiş somut probleme mi dayanıyor?
- Müşteri edinme maliyeti ürün fiyatına göre sürdürülebilir mi?

### 8. Kanıt seviyesini belirle

Kanıtlar güçlüden zayıfa doğru sınıflandırılır:

1. Gerçek ödeme ve tekrar kullanım
2. Ücretli pilot veya bağlayıcı satın alma taahhüdü
3. Hedef müşteriyle yapılan problem görüşmesi
4. Aktif kullanım ve tamamlanan kritik işlem
5. Bekleme listesi veya kayıt
6. Trafik, beğeni ve genel ilgi
7. Kurucunun veya ekibin varsayımı

Karar, eldeki en güçlü kanıt seviyesine göre verilir.

## Karar seçenekleri

### GO — Devam

Problem, ödeme isteği ve ulaşılabilir dağıtım kanalı gerçek davranışlarla doğrulanmıştır. Ürün geliştirme veya ölçekleme mantıklıdır.

### CONDITIONAL GO — Koşullu devam

Problem makuldür fakat ödeme veya dağıtım henüz yeterince doğrulanmamıştır. Sınırlı süre ve bütçeyle deney yapılır; başarı eşiği baştan belirlenir.

### PIVOT — Yön değiştir

Problem gerçektir fakat mevcut ürün, hedef müşteri, değer önerisi, fiyat veya dağıtım yaklaşımı yanlıştır. Korunacak varlıklar ve değiştirilecek varsayımlar açıkça belirtilir.

### NO-GO — Durdur

Problem zayıf, ücretsiz/platform içi alternatif yeterli, ödeme isteği düşük veya ekonomik dağıtım mümkün değildir. Yeni özellik geliştirmeye devam edilmez.

### HOLD — Beklet

Karar dış bir olay veya veriyle anlamlı biçimde değişebilir. Bekleme süresi, izlenecek sinyal ve yeniden değerlendirme tarihi belirlenir. Belirsizliği ertelemek için kullanılmaz.

## Zorunlu deney tasarımı

Koşullu devam veya pivot kararında şu alanlar doldurulur:

- **Ana hipotez:** Müşteri hangi sonuç için para ödeyecek?
- **Hedef segment:** İlk test yapılacak dar müşteri grubu
- **Teklif:** Fiyat ve teslim edilen somut sonuç
- **Kanal:** Müşteriye nasıl ulaşılacak?
- **Örneklem:** Kaç nitelikli müşteriyle temas kurulacak?
- **Süre:** Deney kaç gün sürecek?
- **Başarı eşiği:** Kaç ödeme, pilot veya güçlü taahhüt gerekli?
- **Pivot sinyali:** Hangi davranış farklı bir ürüne işaret eder?
- **Durdurma eşiği:** Hangi sonuçta yeni geliştirme kesilir?

Varsayılan başlangıç deneyi, projeye göre değiştirilmek üzere şöyledir:

- 10 gün
- 50 nitelikli ve kişiselleştirilmiş temas
- En az 10 problem görüşmesi
- En az 3 gerçek ödeme veya eşdeğer ücretli pilot
- Ölçekleme öncesinde en az bir tekrarlanabilir müşteri edinme kanalı

Ücretsiz kullanıcı, e-posta açılması, olumlu yorum veya “ilgilenebilirim” yanıtı ödeme yerine sayılmaz.

## Her proje için kullanılacak rapor formatı

### 1. Yönetici özeti

Projenin ne olduğu ve önerilen karar, en fazla birkaç paragrafta açıklanır.

### 2. Şirketin veya ekibin mevcut kararı

- Ekip hangi kararı vermiş?
- Bu karar hangi kanıtlara ve varsayımlara dayanıyor?
- Karar pazar doğrulamasıyla mı, iç süreç veya teknik ilerlemeyle mi alınmış?

### 3. Ürünün gerçekte sattığı şey

- Görünen özellik
- Müşterinin satın aldığı sonuç
- İddia ile uygulama arasındaki fark

### 4. Pazar ve müşteri ihtiyacı

- Hedef segment
- Problemin aciliyeti ve sıklığı
- Mevcut davranış
- Bilinen veriler
- Bilinmeyenler

### 5. Rakipler ve ikameler

- Doğrudan rakipler
- Ücretsiz/açık kaynak alternatifler
- Platformun yerleşik özellikleri
- Manuel çözüm
- Hiçbir şey yapmama seçeneği

### 6. Güçlü taraflar

Projede korunması gereken teknik, ticari veya dağıtımsal avantajlar açıklanır.

### 7. Kritik riskler

Riskler önem sırasına göre yazılır. Özellikle ödeme isteği, dağıtım, platform riski, hukuki iddia, güvenlik ve ürünün vaat ettiği sonucu gerçekten üretip üretmediği incelenir.

### 8. Karar

Şunlardan biri seçilir:

- GO
- CONDITIONAL GO
- PIVOT
- NO-GO
- HOLD

Kararın nedeni tek ve açık bir paragrafta belirtilir.

### 9. Önerilen konumlandırma

- Kime satılacak?
- Hangi problem üzerinden?
- Hangi sonuç vaat edilecek?
- Hangi ifadelerden kaçınılacak?

### 10. En küçük doğrulama deneyi

- Hipotez
- Segment
- Teklif ve fiyat
- Kanal
- Süre ve örneklem
- Başarı ölçütü

### 11. Devam, pivot ve durdurma eşikleri

Her üçü de sayısal veya açıkça gözlemlenebilir biçimde tanımlanır.

### 12. Öncelikli eylem planı

Yalnızca kararı doğrulamak veya uygulamak için gereken işler sıralanır. Doğrulama olmadan geniş özellik listesi önerilmez.

### 13. Şirkete yazılabilecek karar metni

Konsensüs veya karar günlüğüne doğrudan eklenebilecek kısa İngilizce ya da Türkçe metin hazırlanır.

### 14. Güven seviyesi ve açık sorular

- Kararın güven seviyesi: düşük, orta veya yüksek
- Kararı değiştirebilecek eksik veriler
- Kullanılan önemli kaynaklar ve tarihleri

## AI Disclosure Kit için referans uygulama

Bu çerçevenin AI Disclosure Kit değerlendirmesinde ürettiği karar:

> **CONDITIONAL GO / POSITIONING PIVOT:** Mevcut MVP, sınırlı süreli talep doğrulama deneyi olarak canlıya alınabilir; ancak yalnızca rozet ve sabit metin ürünü olarak ölçeklenmemelidir. Değer önerisi disclosure tespiti, doğru uygulamanın doğrulanması, kanıt geçmişi ve ajans yönetimine kaydırılmalıdır. Elli nitelikli temas içinden en az üç gerçek ödeme veya eşdeğer ücretli pilot alınmadan geniş özellik geliştirmesi yapılmamalıdır.

Bu kararın temel nedenleri:

- Regülasyon gerçek olsa da belirli bir rozet ürünü zorunlu değildir.
- Platformların yerleşik disclosure özellikleri en güçlü ikamedir.
- Ücretsiz ve doğrudan ücretli rakipler mevcuttur.
- Mevcut widget ilk mesajı chatbot içine kendiliğinden yerleştirmemektedir.
- Sadece metin ve rozet kolay metalaşır.
- Doğrulama, kanıt kaydı, sürümleme ve çoklu müşteri yönetimi daha güçlü sürekli değer oluşturabilir.

## Bu belge nasıl kullanılmalı?

Yeni bir proje getirildiğinde şu talimat yeterlidir:

> Bu projeyi `PROJECT_EVALUATION_FRAMEWORK.md` çerçevesine göre araştır, değerlendir ve yönlendir.

Belge aynı çalışma alanında bulunduğu sürece değerlendirme standardı olarak okunmalıdır. Farklı bir repoda veya yeni bir çalışma alanında kullanılacaksa bu dosya da projeye eklenmeli ya da yeniden paylaşılmalıdır.

---

<!-- MOVED HERE FROM PROMPT.md ON 2026-07-29. Kept VERBATIM and in English on
     purpose: this block is a set of gates, and retranslating a gate is how a rule
     quietly changes meaning. It was moved out of the every-cycle prompt because it
     governs discovery, which is currently disabled — but it is NOT conditional on
     that toggle. When discovery runs, this is mandatory reading, exactly as before.
     PROMPT.md points here; do not delete this section without updating that pointer
     and the guardrail check in scripts/core/auto-loop.sh. -->

## SEARCH REGIME — where the company is allowed to win (discovery policy)

Cycles 107–111 showed candidates dying at NATIVE/PLATFORM SUBSTITUTE and TWO-SIDED / TRUST
COLD-START before economics, and this regime was written to kill those shapes earlier. An
independent audit of 61 axes screened in cycles 130–165 (`docs/research/kill-pattern-filter-vs-space-audit-2026-07-25.md`)
found that correction overshot: **0 of ~60 axes survived, and 28 of 61 terminal kills were not
supported by the evidence cited** — 24 premature, 4 unfalsifiable. The regime demanded
validation-grade proof at discovery time, forbade the actions that would produce it, then
treated its absence as a kill. So this block now cuts BOTH ways: kill dead shapes early, but
kill only on affirmative evidence, and let uncertainty travel to economics as UNKNOWN. It
governs only NEWLY-PROPOSED axes at discovery time; it NEVER retro-kills a candidate already
in Selected or Pending Queue.

**Primary generation prior — THREE ARMS, not one.** An audit of 61 screened axes (2026-07-25)
found the single "buyer already pays for the exact task" prior steers generation into mature,
incumbent-heavy categories, which the substitute screen then kills for being mature — a loop
that produced 0 survivors from ~60 axes. Each scan must generate three arms:

1. **Exact-task-spend control** — one axis where the buyer already pays a human, agency, or
   expensive dedicated tool for the exact task.
2. **Adjacent-manual** — one axis where buyers pay for an adjacent manual outcome but no
   dedicated product owns the proposed unit.
3. **Pre-priced remediation** — one publicly pre-priced, event-triggered remediation unit on
   buyer-owned assets (e.g. API/version migration, flaky-test stabilization, schema repair,
   validator-backed artifact remediation, executable-documentation repair, a bounded CI-green
   issue batch). A job posting, bounty, or provider price is CATEGORY and BUYER-BUDGET
   evidence — it is never Auto Company WTP.

Exact-task payment is category evidence, NOT an admission requirement.

**Then bias toward axes with:**
- an OBSERVABLE EXISTING BUDGET for the outcome (revealed money, not a trivial platform fee);
- an ACCRETIVE ASSET the company's own WORK builds and keeps current (aggregation/freshness
  labor arbitrage), NOT pre-existing proprietary data it cannot have on day one;
- real PRICE TOLERANCE (the credible alternative is expensive, leaving room beneath it);
- a CHANNEL that is an existing self-serve marketplace or organic-intent surface with a
  built-in payment rail the company can list on for free. Channel-first orders discovery
  SEQUENCING only — it does not re-rank the GO criteria (WTP still dominates channel). A
  prospect list, hypothetical cold outreach, or a plan to build an audience does NOT count as
  an existing channel. Any later outreach, listing, or payment action remains governed by the
  current authorization and WTP rules; this discovery preference authorizes none;
- NATURAL REPEAT purchase — a tie-breaker between otherwise-comparable axes, not a gate.

**Early substitute / cold-start kill (BEFORE deep research).** Kill for substitute dominance
ONLY when current evidence shows a NAMED substitute serves the same buyer, the same triggering
context, the same required inputs/access, and the same end-to-end acceptance unit, at equal or
lower total cost and switching burden. Feature overlap, category presence, "an incumbent
exists", or the platform merely owning the source context is NOT sufficient — the audit found
this label applied to 38 of 42 axes while only 26 actually died of substitution. Also kill if
the offer needs a TWO-SIDED / network / trust cold-start the company cannot seed. Log the
driver.

**Missing evidence is UNKNOWN, not a kill.** Absence of a public counter-observation proves
nothing. Kill only on (a) affirmative end-to-end substitute dominance as defined above,
(b) fatal authority/licensing exposure, or (c) a necessary network dependency that cannot be
seeded. Otherwise record the axis as **UNKNOWN / VALIDATION-REQUIRED** and send it to
economics. That status authorizes NO build, outreach, listing, payment, or fulfillment.

**Acceptance is the contracted deliverable, not the buyer's downstream outcome.** Acceptance
may be defined by enumerated deliverables, source-population coverage, executable tests,
evidence links, revision caps, and buyer sign-off. Do NOT require a grant win, a funding
round, a CTR improvement, a platform reinstatement, or a regulator decision unless the offer
explicitly guarantees that result. Likewise, "the customer could be harmed if this is done
badly" is ordinary commercial reliance — it is a licensing veto only where a licensed
professional's judgement or sign-off is legally required.

**Wedge gate — kill-reason-specific and falsifiable.** For every early kill condition
triggered, name a direct counter-observation and the observation that would falsify it. A
channel or observed budget can clear ONLY channel/budget risk; it CANNOT override a dominant
native substitute. To clear native-substitute dominance, show the material paid outcome the
substitute fails to deliver and why the proposed accretive asset, freshness advantage,
comprehensiveness, liability transfer, or switching cost closes that exact gap. Existing
competitor payment for the same wedge is supporting evidence where it happens to exist.

**Discovery admission must NOT demand validation evidence.** Do not require three paying
buyers, visible repeat purchases, buyer-authored incumbent-failure text, or a zero-review
entrant win to admit an axis. Those are VALIDATION evidence, and the company is not
authorized to go and collect them — demanding them at discovery time, then killing for their
absence, is the closed loop the audit identified. When an axis is economically plausible but
the deciding action is unauthorized, mark it **TEST-BLOCKED / PENDING operator review**, not
KILLED.

NO QUALIFYING CANDIDATE remains a valid, expected outcome of this screen — do NOT manufacture
a wedge to keep the board non-empty. This refines discovery only; it changes NOTHING about
the WTP HARD STOP, the dedup gate, or authorization.

**Reusable asset — TIE-BREAKER, not a generation constraint.** Where an axis would let each
future paid fulfillment add a named REUSABLE ASSET (dataset, taxonomy, rule library,
benchmark, test corpus) that lowers future marginal cost, prefer it over an otherwise-equal
axis, and state the asset, accumulation unit, reuse path, and falsifier. The ABSENCE of an
immediate reusable asset is NOT a discovery kill — as a generation constraint this prior was
one of the sentences producing the single "productized desk" shape across ~60 axes. It applies
only among axes that already survive structural screening and economics, and authorizes no
build, fulfillment, outreach, or payment action.

**Durable decision ledger — every screened axis, including pre-extraction kills.** Append one
row per axis to `memories/decision-ledger.md` with: stable axis ID · buyer × delivery shape ×
price · exactly ONE primary kill code · primary-source citations · status (`CONFIRMED KILL` /
`UNKNOWN` / `TEST-BLOCKED` / `ECONOMIC PASS` / `ECONOMIC FAIL`) · the falsifier. Scans are
rotated away; the ledger is the only durable record, and without it the company keeps
re-deriving conclusions from its own lost output. A row with no primary source, no kill code,
or two kill codes is INVALID — fix it rather than leaving it. Note that the archive and the
exhausted-pattern list are outputs of THIS screen: they corroborate nothing about its accuracy.

**Pricing-structure gate — a routing rule, NOT a kill or a flat-fee ban.** The 2026-07-25
10-cycle filter-vs-space experiment beat both CFO-gate targets (near-miss 5/9, remediation
9/10) but logged 0/14 economic passes under inconsistent, non-comparable CFO inputs. An
independent high-model review (`docs/research/filter-vs-space-pricing-decision-2026-07-25.md`)
found this does NOT prove flat-fee pricing is structurally dead — it found the 14 verdicts used
different hourly rates, reserve treatment, and CAC assumptions, and only ONE axis (176-R)
survives as a genuine pricing-architecture question once normalized. For any FIXED-PRICE
service whose acceptance depends on repairing a buyer-controlled artifact, an item-count cap
ALONE does not bound cost. Before recording `ECONOMIC PASS`: identify the actual effort driver
and show it is either observable before acceptance, or contractually capped without unpaid
completion/refund exposure. Apply the standing CFO model unchanged — all person-time at
$50/hour, nonzero evidenced AI/tool cost, processing, the 10% pre-observation reserve, the
prescribed base/stress test, and evidenced or conservatively modeled CAC with
Contribution:CAC ≥3:1; UNKNOWN CAC blocks PASS. If the effort driver is unknown, route to
**`PRICING-STRUCTURE UNKNOWN / TEST-BLOCKED`** and compare structures — e.g. a prequalified
fixed tier, a diagnostic-plus-firm-quote, or buyer-approved overage — rather than accepting or
killing the raw flat-fee offer. Do NOT kill the axis, ban flat fees as a category, price by a
raw item count uncorrelated with effort, or infer build/outreach/payment authority from this
gate — those remain governed by the HARD STOP below and the single active-validation slot.
Each fresh axis gets AT MOST ONE bounded pricing-architecture adjudication without new primary
evidence — if it stays `TEST-BLOCKED`, queue it and return to discovery; do not re-model the
same axis again absent new evidence or an explicit operator directive, or "normal discovery"
degrades into a repeating two-cycle pricing-adjudication loop.

