<p align="center">
  <img src="https://c.tenor.com/12303175589018653718/tenor.gif" width="300" alt="Sonic" />
</p>

<h1 align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2000&pause=400&color=FFCC00&center=true&vCenter=true&width=650&lines=%F0%9F%91%BB+WHM+GHOST+v1.0+Auto;Root+Oturum+Atlama+S%C3%BCper+H%C4%B1zl%C4%B1;Geli%C5%9Ftirici%3A+Arsenik" alt="Typing SVG" />
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python&style=for-the-badge" />
  <img src="https://img.shields.io/badge/S%C3%BCr%C3%BCm-v1.0%20Auto-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/CVSS-10.0-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Lisans-MIT-green?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Geli%C5%9Ftirici-Arsenik-black?style=for-the-badge" />
  <br/>
  <img src="https://img.shields.io/badge/H%C4%B1z-Sonic%20Seviyesi-blueviolet?style=flat-square" />
  <img src="https://img.shields.io/badge/Ba%C4%9F%C4%B1ml%C4%B1l%C4%B1k-S%C4%B1f%C4%B1r-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/Exploit-CRYP%20Injection-critical?style=flat-square" />
</p>

<br />

## 🦔 WHM Ghost – Sonic Hızında Root Erişimi

**WHM Ghost**, cPanel ve WHM sunucularında bulunan **CVE-2026-41940**  
kimlik doğrulama atlama zaafiyetini **(CVSS 10.0)** sömürmek için geliştirilmiş  
**tam otomatik, sıfır bağımlılık** bir penetrasyon testi aracıdır.  
Hedefi verin; dört aşamalı exploit zinciri **Sonic hızıyla** çalışsın,  
ardından sistem bilgilerini toplasın, isterseniz interaktif bir root shell açsın.

> 💨 **“Hayalet gibi sız, Sonic gibi kaç.”**  
> 🧠 Geliştirici: **Arsenik**

---

## 🔥 Neden WHM Ghost?

| Avantaj | Detay |
|--------|--------|
| 🚀 **Sonic Hızı** | Çoklu iş parçacığıyla yüzlerce hedefi aynı anda tarar |
| 🧠 **Tam Otomatik** | 4 aşamalı zincir + keşif + rapor – tek komutla |
| 🐍 **Sıfır Bağımlılık** | Python 3.6+ dışında hiçbir şey yüklemezsiniz |
| 📡 **Pipeline Hazır** | Shodan, subfinder, httpx çıktılarını doğrudan boru ile alır |
| 💬 **Zengin Açıklamalar** | Her aşama renkli log'larla canlı canlı anlatılır |
| 💻 **Root Shell** | Başarı anında interaktif terminal, dosya okuma, komut çalıştırma |
| 📄 **JSON Rapor** | Tüm bulguları yapılandırılmış olarak dışa aktar |

---

## 🧩 CVE-2026-41940 Nedir?

### ⚠️ Zafiyet Özeti

cPanel & WHM, oturum dosyasını kaydettikten **sonra** `filter_sessiondata()` fonksiyonunu çağırır.  
Bu zamanlama hatası, **Authorization başlığına** CRLF karakterleri enjekte ederek oturum dosyasına **hasroot=1**, **tfa_verified=1** gibi yetkili alanlar yazılmasına izin verir.  
Sonuç: **tam root erişimi**.

### 💥 Etkileri

- Geçerli bir kullanıcı adı‑parola bilmeden WHM arayüzüne root olarak girebilirsiniz.
- API üzerinden tüm sunucuyu yönetebilir; hesap oluşturma, silme, şifre değiştirme, komut çalıştırma.
- Arka kapı bırakıp kalıcı erişim sağlanabilir.

### 📦 Etkilenen Sürümler

| Sürüm Dalı | Yamalı Yapı |
|------------|--------------|
| 11.110 | < 11.110.0.97 |
| 11.118 | < 11.118.0.63 |
| 11.126 | < 11.126.0.54 |
| 11.132 | < 11.132.0.29 |
| 11.134 | < 11.134.0.20 |
| 11.136 | < 11.136.0.5 |

> ✅ Düzeltme: `Session.pm` içinde `saveSession()` fonksiyonundaki filtreleme, **dosyaya yazmadan önce** yapılacak şekilde düzeltildi.

---

## 🔗 4 Aşamalı Saldırı Zinciri

Araç, sıfırdan root'a giden yolu adım adım otomatik olarak işler:
