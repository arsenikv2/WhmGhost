<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2500&pause=500&color=FF6E4A&center=true&vCenter=true&width=650&lines=%F0%9F%91%BB+WHM+GHOST+v1+Auto;Root+oturum+atlama+tam+otomatik;Geli%C5%9Ftirici%3A+Arsenik" />
    <source media="(prefers-color-scheme: light)" srcset="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2500&pause=500&color=0D1117&center=true&vCenter=true&width=650&lines=%F0%9F%91%BB+WHM+GHOST+v1+Auto;Root+oturum+atlama+tam+otomatik;Geli%C5%9Ftirici%3A+Arsenik" />
    <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2500&pause=500&color=FF6E4A&center=true&vCenter=true&width=650&lines=%F0%9F%91%BB+WHM+GHOST+v1+Auto;Root+oturum+atlama+tam+otomatik;Geli%C5%9Ftirici%3A+Arsenik" alt="WHM Ghost" />
  </picture>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python&style=for-the-badge" />
  <img src="https://img.shields.io/badge/S%C3%BCr%C3%BCm-v1.0%20Auto-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/CVSS-10.0-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Lisans-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Geli%C5%9Ftirici-Arsenik-black?style=for-the-badge" />
</p>

<p align="center">
  <b>CVE-2026-41940</b> · cPanel & WHM CRLF Injection → Full Root Takeover<br />
  <sub>Tam otomatik · Sıfır bağımlılık · Efsane hız</sub>
</p>

<br />

## 📺 Canlı Demo (GIF)

<p align="center">
  <img src="https://user-images.githubusercontent.com/demo/whm-ghost-demo.gif" width="720" alt="WHM Ghost Demo" />
  <br />
  <sub>⬆ Hedefi ver, arkana yaslan – Ghost her şeyi halleder.</sub>
</p>

---

## 🔥 Nedir Bu?

**WHM Ghost**, cPanel & WHM sunucularındaki **CVE-2026-41940**  
kimlik doğrulama atlama zaafiyetini **(CVSS 10.0)** sonuna kadar sömürmek için yazılmıştır.  
4 aşamalı exploit zincirini tek bir tuşla çalıştırır, başarılı olursa:

- Hedef sistemde **root yetkisiyle** bilgi toplar,
- Hesap listelerini çeker,
- İsterseniz interaktif bir **root shell** açar,
- Sonuçları **JSON** dosyasına yazar.

> **Hayalet gibi sız, iz bırakma.** 👻

---

## ✨ Öne Çıkan Özellikler

| ⚙️ Teknik | 🧠 Zeka |
|----------|---------|
| `Stage 0` Canonical host keşfi | Yanlış Host başlığı varsa otomatik düzeltir |
| `Stage 1` Preauth oturumu | Sadece yanlış parolayla oturum çalar |
| `Stage 2` CRLF enjeksiyonu | `hasroot=1` alanını oturum dosyasına yazar |
| `Stage 3` Propagasyon | Token‑denied tuzağı ile önbelleğe iter |
| `Stage 4` Doğrulama | `/json-api/version` yanıtı ile root erişimi teyit eder |
| **Otomatik keşif** | Hesaplar, sunucu bilgisi, disk, yük |
| **Pipeline uyumlu** | Shodan, subfinder, httpx çıktılarını doğrudan yer |
| **Interaktif Shell** | `cat`, `exec`, `passwd`, `addadmin` – hepsi root yetkisiyle |
| **JSON rapor** | Tüm bulgular `-o` ile yapılandırılmış olarak kaydedilir |

---

## 🚀 Hızlı Başlangıç

```bash
git clone https://github.com/arsenik/whm-ghost.git
cd whm-ghost
python3 whm_ghost.py -u https://hedef.com:2087

