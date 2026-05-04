<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python" />
  <img src="https://img.shields.io/badge/Sürüm-1.0%20Auto-orange" />
  <img src="https://img.shields.io/badge/CVSS-10.0-red" />
  <img src="https://img.shields.io/badge/Lisans-MIT-green" />
  <img src="https://img.shields.io/badge/Geliştirici-Arsenik-black" />
</p>

<h1 align="center">👻 WHM Ghost</h1>
<h3 align="center">CVE-2026-41940 · cPanel & WHM Oturum Çalma → Root</h3>
<p align="center"><b>Tam otomatik, sıfır bağımlılık, efsanevi hız.</b></p>

<br />

## 🌌 Nedir?

**WHM Ghost**, cPanel / WHM sunucularında **CVSS 10.0** olarak derecelendirilen  
**CVE-2026-41940** kimlik doğrulama atlama açığını kullanan **pentest aracıdır**.  
Hedefi verin; tüm saldırı zincirini (4 aşamalı), keşfi ve raporlamayı sizin için otomatik yapsın.

> **“Hayalet gibi içeri sız, gölge bırakma.”**

<br />

## ✨ Öne Çıkanlar

- ⚡ **Tam Otomatik Pilot** – Exploit → Keşif → Rapor tek komutla
- 🧩 **Modüler Yapı** – Sadece istediğin adımı çalıştır
- 🐍 **Python 3.6+** – Hiçbir pip paketine ihtiyaç duymaz
- 🌐 **WHM JSON‑API** – Hesap listeleme, komut çalıştırma, şifre değiştirme
- 📡 **Pipeline Hazır** – Shodan, subfinder, httpx çıktıları ile beslenebilir
- 🧵 **Multithreading** – 20+ hedefi aynı anda işleyin
- 💻 **Root Shell** – Başarılı exploit sonrası interaktif terminal
- 📂 **JSON Rapor** – Tüm bulguları yapılandırılmış olarak dışa aktar

<br />

## 📦 Kurulum

```bash
# Repoyu klonla
git clone https://github.com/arsenik/whm-ghost.git
cd whm-ghost

# Çalıştır (sanallaştırma opsiyonel)
python3 whm_ghost.py -u https://hedef.com:2087

