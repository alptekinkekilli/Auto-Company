"""OPEX RFQ e-posta metni — SADECE İÇERİK (güvenlik-hassas değil, protected DEĞİL).

Serbestçe iterasyon: rfq-send.py bu modülden subject()/body()/SCOPE'u import eder; send
mantığı (§15 gate, caps, teslim) rfq-send.py'da (protected) kalır. Böylece metni prod-marker
sürtünmesi olmadan iyileştirebiliriz.

Ton: sıcak, insani, net — hukuk dili YOK ("müvekkil" vb. kullanma). Appricode, danışmanlığını
yürüttüğü kurulmakta-olan bir araç-finansmanı girişimi için indikatif fiyat toplar; girişimin
adı paylaşılmaz (anonim — yalnız sektör + teknik ihtiyaç). İmza Appricode'undur (müşteri değil).
"""

# ── kümeye-özel ihtiyaç metni (anonim — stratejik hacim/marka YOK) ────────────────
SCOPE = {
 "bulut-güvenlik": "Web tabanlı bir finansal operasyon paneli ve veri servisleri için üretim "
    "ve test ortamı. Verilerin Türkiye'de tutulması (KVKK/regülasyon) bizim için zorunlu; "
    "yedekli mimari, izleme ve felaket-kurtarma bekliyoruz. Güvenlik tarafında ise yedekleme "
    "(RPO/RTO hedefli), SOC/izleme ve yıllık sızma testi. Ölçek orta düzeyde başlıyor, aşamalı "
    "büyümeye açık.",
 "erp-efatura": "Muhasebe/finans, cari hesap, sabit kıymet ve raporlama modülleri; VUK / "
    "e-defter uyumu. Ayrıca e-Fatura / e-Arşiv / e-İmza / KEP entegrasyonu. Ekip kuruluş "
    "aşamasında küçük ama büyümeye açık; belge hacmi orta düzeyde.",
 "kira": "İstanbul'da esnek/hazır ofis. Küçük bir ekiple başlıyoruz; 6-12 ay içinde büyümeye "
    "açık, koltuk/özel oda eklenebilen bir düzen arıyoruz. Toplantı odası, internet, resepsiyon "
    "ve aidatın dahil olması bizim için önemli. Tercihimiz merkezi iş bölgeleri (Levent, Maslak, "
    "Ataşehir gibi) — teklifinizde bölgeyi belirtmenizi rica ederiz.",
 "pazarlama": "Üç ihtiyacımız var: (a) marka kimliği ve konumlandırma, (b) PR / lansman ve "
    "medya ilişkileri, (c) dijital performans (edinim). Sektör finansal hizmet. Gerekirse "
    "gizlilik sözleşmesi (NDA) imzalamaya açığız.",
 "sigorta": "Üç başlıkta teklif rica ediyoruz: Kurumsal (işyeri, siber sorumluluk, mesleki "
    "sorumluluk), Araç (finanse edilen araçlar için kasko + trafik, portföy bazlı) ve Alacak "
    "(alacak/kredi sigortası). Kuruluş aşamasındayız; araç ve alacak tarafında hacim gerektiren "
    "detayları NDA / anonim profil ile paylaşabiliriz.",
}

SIGNATURE = (
 "Sevgiler,\n"
 "Appricode · Tedarik & İş Geliştirme\n"
 "tedarik@go.appricode.tr · appricode.tr"
)
# NOT: İstenirse buraya kişi adı + telefon eklenebilir (yanıt oranını artırır).


def subject(kume: str) -> str:
    return f"{kume} için fiyat teklifi alabilir miyiz?"


def body(kume: str, scope: str) -> str:
    return (
        "Merhaba,\n\n"
        "Ben Appricode'dan yazıyorum. Şu sıralar, kurulum aşamasındaki bir araç-finansmanı "
        "girişiminin tedarik hazırlığını yürütüyoruz ve bu kapsamda sizden "
        f"{kume.lower()} tarafında kısa bir indikatif fiyat teklifi rica edeceğiz. Girişimin "
        "adını bu aşamada paylaşamıyoruz; ihtiyacın sektörünü ve teknik çerçevesini aşağıda "
        "bulabilirsiniz.\n\n"
        f"İhtiyacımız:\n{scope}\n\n"
        "Teklifte şunlar bize çok yardımcı olur:\n"
        "• Aylık / birim indikatif fiyat (KDV hariç)\n"
        "• Fiyatın dayandığı varsayımlar ve varsa hacim kademeleri\n"
        "• Varsa kurulum / tek seferlik maliyetler\n"
        "• Teklifin geçerlilik süresi\n\n"
        "Bu bir ön araştırma; bağlayıcı bir sipariş değil. Uygun olursa kısa bir görüşme de "
        "yapabiliriz. Ayıracağınız vakit için şimdiden teşekkür ederiz.\n\n"
        + SIGNATURE + "\n"
    )
