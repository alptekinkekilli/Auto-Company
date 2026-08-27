"""OPEX RFQ e-posta metni + imza — SADECE İÇERİK (güvenlik-hassas değil, protected DEĞİL).

Serbestçe iterasyon: rfq-send.py buradan subject()/body()/body_html()/SCOPE/attachments()
import eder; send mantığı (§15 gate, caps, teslim) rfq-send.py'da (protected) kalır.

Ton: sıcak ama profesyonel, hukuk dili YOK. Appricode, danışmanlığını yürüttüğü kurulmakta-olan
bir araç-finansmanı girişimi için indikatif fiyat toplar; girişimin marka/şirket adı paylaşılmaz
(anonim — yalnız sektör + teknik kapsam). İmza Appricode'undur (müşteri değil).

Logo Gmail'de base64 data-URI olarak GÖSTERİLMEZ; bu yüzden CID inline attachment olarak gider
(attachments()) ve HTML imza src="cid:appricode-logo" kullanır.
"""
import os as _os
import re as _re

LOGO_CID = "appricode-logo"

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

# Düz-metin imza (text/plain parçası).
SIGNATURE = (
 "Saygılarımızla,\n"
 "Alptekin Kekilli — Founder & Managing Partner\n"
 "Appricode LLC\n"
 "M +90 546 645 64 79 · E alp@appricode.tr · W appricode.tr\n"
 "Piyalepaşa Blv. No:71 Kat:11, Şişli, İstanbul"
)

_SIG_PATH = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "rfq_signature.html")


def _read_sig() -> str:
    try:
        return open(_SIG_PATH, encoding="utf-8").read()
    except OSError:
        return ""


def _logo_b64() -> str:
    m = _re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", _read_sig())
    return m.group(1) if m else ""


LOGO_B64 = _logo_b64()


def _html_signature() -> str:
    """<body> içi; base64 data-URI'yi cid:appricode-logo ile değiştir (Gmail base64 göstermez)."""
    doc = _read_sig()
    if not doc:
        return "<pre>" + SIGNATURE + "</pre>"
    m = _re.search(r"<body[^>]*>(.*)</body>", doc, _re.S | _re.I)
    inner = (m.group(1) if m else doc).strip()
    return _re.sub(r'src="data:image/png;base64,[A-Za-z0-9+/=]+"',
                   f'src="cid:{LOGO_CID}"', inner)


HTML_SIGNATURE = _html_signature()


def attachments() -> list:
    """CID inline logo — send_fe JSON body'sine eklenir. Logo yoksa boş liste."""
    if not LOGO_B64:
        return []
    return [{"filename": "appricode-logo.png", "content": LOGO_B64,
             "encoding": "base64", "cid": LOGO_CID, "contentType": "image/png"}]


_BULLETS = (
 "Aylık ve/veya birim fiyatlar (KDV hariç)",
 "Fiyatlandırma varsayımları ve varsa hacim bazlı kademeler",
 "Kurulum veya diğer tek seferlik maliyetler",
 "Teklifin geçerlilik süresi",
)


def subject(kume: str) -> str:
    return f"{kume} kapsamında indikatif fiyat teklifi talebi"


def body(kume: str, scope: str) -> str:
    bul = "".join("• " + b + "\n" for b in _BULLETS)
    return (
        "Merhaba,\n\n"
        "Appricode olarak, kuruluş aşamasındaki araç finansmanı odaklı bir girişim için tedarik "
        f"hazırlığı yürütüyoruz. Bu kapsamda, {kume.lower()} alanındaki ihtiyaçlarımız için sizden "
        "ön değerlendirmeye yönelik indikatif bir fiyat teklifi rica etmek isteriz.\n\n"
        "Girişimin marka ve şirket bilgilerini bu aşamada paylaşamıyoruz; ancak ihtiyaç duyulan "
        "sektör ve teknik kapsam aşağıdadır:\n\n"
        f"İhtiyaç kapsamı:\n{scope}\n\n"
        "Teklifinizde aşağıdaki bilgileri paylaşmanız bizim için faydalı olacaktır:\n"
        f"{bul}\n"
        "Bu çalışma, şu aşamada bağlayıcı bir sipariş niteliği taşımayan bir ön araştırmadır. "
        "Uygun olmanız halinde, ihtiyaçları kısaca değerlendirmek üzere bir görüşme de "
        "planlayabiliriz.\n\n"
        "Zaman ayırdığınız için teşekkür eder, geri dönüşünüzü bekleriz.\n\n"
        + SIGNATURE + "\n"
    )


def body_html(kume: str, scope: str) -> str:
    sc = scope.replace("&", "&amp;").replace("<", "&lt;")
    bul = "".join(f"<li>{b}</li>" for b in _BULLETS)
    return (
        '<div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;line-height:1.55;color:#222222;">'
        "<p>Merhaba,</p>"
        "<p>Appricode olarak, kuruluş aşamasındaki <b>araç finansmanı</b> odaklı bir girişim için "
        f"tedarik hazırlığı yürütüyoruz. Bu kapsamda, {kume.lower()} alanındaki ihtiyaçlarımız için "
        "sizden ön değerlendirmeye yönelik <b>indikatif</b> bir fiyat teklifi rica etmek isteriz.</p>"
        "<p>Girişimin marka ve şirket bilgilerini bu aşamada paylaşamıyoruz; ancak ihtiyaç duyulan "
        "sektör ve teknik kapsam aşağıdadır:</p>"
        f"<p><b>İhtiyaç kapsamı:</b><br>{sc}</p>"
        "<p>Teklifinizde aşağıdaki bilgileri paylaşmanız bizim için faydalı olacaktır:</p>"
        f"<ul>{bul}</ul>"
        "<p>Bu çalışma, şu aşamada bağlayıcı bir sipariş niteliği taşımayan bir <b>ön "
        "araştırmadır</b>. Uygun olmanız halinde, ihtiyaçları kısaca değerlendirmek üzere bir "
        "görüşme de planlayabiliriz.</p>"
        "<p>Zaman ayırdığınız için teşekkür eder, geri dönüşünüzü bekleriz.</p>"
        '<div style="margin-top:18px;">' + HTML_SIGNATURE + "</div>"
        "</div>"
    )
