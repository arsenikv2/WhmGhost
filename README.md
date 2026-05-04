<p align="center">
  <svg width="700" height="200" viewBox="0 0 700 200" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#ff6e4a"/>
        <stop offset="50%" stop-color="#ffcc00"/>
        <stop offset="100%" stop-color="#ff6e4a"/>
      </linearGradient>
      <mask id="m">
        <rect x="0" y="0" width="700" height="200" fill="black"/>
        <rect x="0" y="0" width="0" height="200" fill="white">
          <animate attributeName="width" from="0" to="700" dur="2s" fill="freeze"/>
        </rect>
      </mask>
    </defs>
    <rect width="700" height="200" fill="transparent"/>
    <text x="350" y="90" text-anchor="middle" font-family="monospace" font-size="42" font-weight="bold"
          fill="url(#g)" mask="url(#m)">
      👻 WHM GHOST
    </text>
    <text x="350" y="150" text-anchor="middle" font-family="monospace" font-size="20" fill="#8899aa" opacity="0">
      CVE-2026-41940 · Tam Otomatik Root Avı
      <animate attributeName="opacity" from="0" to="1" begin="2.5s" dur="1.5s" fill="freeze"/>
    </text>
    <text x="350" y="180" text-anchor="middle" font-family="monospace" font-size="16" fill="#667788" opacity="0">
      Developed by Arsenik
      <animate attributeName="opacity" from="0" to="1" begin="3.5s" dur="1s" fill="freeze"/>
    </text>
  </svg>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python&amp;style=for-the-badge" />
  <img src="https://img.shields.io/badge/S%C3%BCr%C3%BCm-v1.0%20Auto-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/CVSS-10.0-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Lisans-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Geli%C5%9Ftirici-Arsenik-black?style=for-the-badge" />
</p>

<br />

## 🔥 Ne Yapar?

| Hedefi ver, arkanıza yaslanın – Ghost saniyeler içinde |
|--------------------------------------------------------|
| 🔓 **4 aşamalı zincirle** cPanel/WHM'de **root oturum çalar** |
| 📊 Başarılı olursa otomatik **hesap listesi, sunucu bilgisi, rapor** çıkarır |
| 💻 İstersen **interaktif root shell** açar |
| 🧵 Eş zamanlı tarama ile **yüzlerce hedefi** işleyebilir |
| 🐍 Sıfır bağımlılık – **sadece Python 3.6+** |

---

## 🚀 Hızlı Başlangıç

```bash
git clone https://github.com/arsenik/whm-ghost.git
cd whm-ghost
python3 whm_ghost.py -u https://hedef.com:2087
