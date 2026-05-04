
> ⚡ **CVE-2026-41940** | cPanel & WHM Oturum Çalma → Root Erişimi  
> 🧠 Geliştirici: **Arsenik**  
> 🔥 **Tam Otomatik** · Modüler · Stdlib Tabanlı · Sıfır Bağımlılık  

[![Python](https://img.shields.io/badge/Python-3.6%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](#lisans)
[![Version](https://img.shields.io/badge/Version-1.0%20Auto-orange)](#)
[![CVSS](https://img.shields.io/badge/CVSS-10.0-red)](#)

---

## 📖 Hakkında

**WHM Ghost**, cPanel/WHM sunucularında kritik bir kimlik doğrulama atlama (CVSS 10.0) zaafiyeti olan **CVE-2026-41940**'ı otomatik olarak sömüren, ardından otomatik keşif ve raporlama yapan bir **pentest aracıdır**.  

Hiçbir harici bağımlılık gerektirmez; Python 3.6+ ile çalışır.  
**Sadece hedefi verin, gerisini Ghost halleder.** 👻

---

## ✨ Özellikler

- 🔓 **4 Aşamalı Exploit Zinciri** (Preauth → CRLF Enjeksiyon → Propagate → Doğrulama)
- 🤖 **Tam Otomatik Mod**: Exploit → Keşif → Rapor tek komutta
- 📡 **WHM API Entegrasyonu**: Hesap listeleme, sunucu bilgisi, komut çalıştırma
- 🕵️ **Sessiz Tarama**: Sadece başarılı hedefleri raporlar, log'lar renklidir
- 📂 **JSON Çıktı**: Sonuçları dosyaya yaz, CI/CD'ye entegre et
- 🧩 **Pipeline Desteği**: `subfinder`, `httpx`, `shodan` gibi araçlarla besle
- 🌐 **SSL/TLS Yönetimi**: Kendi SSL konteksini oluşturur, sertifika hatalarını atlar
- 💻 **İnteraktif Shell**: Root yetkisiyle komut çalıştırma, dosya okuma, şifre değiştirme
- 🚀 **Multithreading**: Toplu taramalarda yüksek hız

---

## 📦 Gereksinimler

- Python **3.6+** (önerilen 3.8+)
- **pip paketi zorunlu değildir** – tüm kod `stdlib` ile yazılmıştır.

> `requirements.txt` dosyası opsiyoneldir, sadece belgeleme amaçlıdır.

---

## 🛠️ Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/arsenik/whm-ghost.git
cd whm-ghost

# (Opsiyonel) Sanal ortam oluşturun
python3 -m venv venv
source venv/bin/activate

# Aracı çalıştırın
python3 whm_ghost.py -u https://hedef.com:2087

graph TD
    A[🎯 Hedef URL] --> B{WHM Ghost v1 Auto}
    B --> C[Stage 0: Canonical Host Keşfi]
    C --> D[Stage 1: Preauth Session Al]
    D --> E[Stage 2: CRLF Enjeksiyon]
    E --> F[Stage 3: Cache Propagate]
    F --> G[Stage 4: Root Erişim Doğrula]
    G --> H{Doğrulandı mı?}
    H -->|Evet| I[🔍 Otomatik Keşif]
    I --> J[📄 JSON Rapor]
    J --> K[✅ Tamamlandı]
    H -->|Hayır| L[❌ Hata Logu]
