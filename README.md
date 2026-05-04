<br />

<p align="center">
  <b>CVE-2026-41940</b> · cPanel & WHM CRLF Injection → Root Bypass<br />
  <sub>CVSS 10.0 · Tam Otomatik · Sıfır Bağımlılık</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-3776AB?logo=python&logoColor=white&style=flat-square" />
  <img src="https://img.shields.io/badge/Sürüm-1.0_Auto-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/CVSS-10.0-red?style=flat-square" />
  <img src="https://img.shields.io/badge/Lisans-MIT-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Arsenik-000?style=flat-square" />
</p>

---

**WHM Ghost**, cPanel/WHM sunucularında **CVE-2026-41940** kimlik doğrulama atlamasını 
**tam otomatik** olarak sömürür. Hedefi verin; 4 aşamalı exploit, keşif ve rapor 
kendiliğinden çalışır — başarılı olursa **root shell** hazırdır.  
Yalnızca **Python 3.6+** gerektirir, hiçbir harici paket kurulmaz.

---

## Zafiyet Detayı

`saveSession()` fonksiyonu, oturum dosyasını yazdıktan **sonra** filtreleme yapar.  
**Authorization: Basic** başlığına yerleştirilen CRLF karakterleri, oturum dosyasına 
`hasroot=1`, `tfa_verified=1` gibi yetki alanlarını enjekte eder.  
→ **Geçersiz parolayla dahi root erişimi sağlanır.**

**Etkilenen:** 11.110.0.97, 11.118.0.63, 11.126.0.54, 11.132.0.29, 11.134.0.20, 11.136.0.5 öncesi tüm yapılar.  
**Düzeltme:** `Session.pm` içinde filtreleme, yazma işleminden önce yapılmaya başlandı.

---

## Saldırı Zinciri

| Aşama | Eylem | Amaç |
|-------|--------|------|
| **Stage 0** | `/openid_connect/cpanelid` → 307 | Gerçek sunucu adını keşfet |
| **Stage 1** | `POST /login/?login_only=1` yanlış parola | Preauth oturum çerezi al |
| **Stage 2** | `GET /` + CRLF'li Authorization | Oturum dosyasına `hasroot=1` yaz |
| **Stage 3** | `GET /scripts2/listaccts` | Token-denied tuzağı → önbelleğe it |
| **Stage 4** | `GET /cpsess.../json-api/version` | Root erişimini doğrula |

<br />

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=26&duration=2000&pause=600&color=FF9900&center=true&vCenter=true&width=600&lines=%F0%9F%91%BB+WHM+GHOST+v1.0+Auto;cPanel+%2F+WHM+Root+Auth+Bypass;Geli%C5%9Ftirici:+Arsenik" alt="Ghost" />
</p>

<p align="center">
  <b>CVE-2026-41940</b> · CRLF Injection → Full Root Takeover<br/>
  <sub>CVSS 10.0 &nbsp;|&nbsp; Tam Otomatik &nbsp;|&nbsp; Sıfır Bağımlılık &nbsp;|&nbsp; Python 3.6+</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.6+-blue?logo=python&style=flat-square" />
  <img src="https://img.shields.io/badge/S%C3%BCr%C3%BCm-1.0_Auto-orange?style=flat-square" />
  <img src="https://img.shields.io/badge/CVSS-10.0-red?style=flat-square" />
  <img src="https://img.shields.io/badge/Lisans-MIT-success?style=flat-square" />
  <img src="https://img.shields.io/badge/Geli%C5%9Ftirici-Arsenik-000?style=flat-square" />
</p>

---

**WHM Ghost**, cPanel & WHM sunucularındaki kritik **CVE-2026-41940** zafiyetini
tam otomatik olarak sömüren bir pentest aracıdır.  
Hedefi verin – dört aşamalı exploit zinciri saniyeler içinde çalışır,  
sunucudan bilgi toplar ve isteğe bağlı olarak **root shell** açar.  
Hiçbir ek paket gerektirmez, yalnızca **Python 3.6+** yeterlidir.

---

## Zafiyet Özeti

cPanel’ın `saveSession()` fonksiyonu, oturum dosyasını diske yazdıktan **sonra** 
filtreleme yapar. Bu zamanlama hatası sayesinde **Authorization** başlığına 
CRLF karakterleri enjekte edilerek dosyaya **hasroot=1** değeri yazılır.
Böylece **geçersiz bir parola ile bile root erişimi** kazanılır.

| Etkilenen Sürümler | Düzeltme |
|---------------------|----------|
| 11.110.0.x < 97    | `Session.pm` içinde filtreleme artık yazmadan önce yapılır. |
| 11.118.0.x < 63    |  |
| 11.126.0.x < 54    |  |
| 11.132.0.x < 29    |  |
| 11.134.0.x < 20    |  |
| 11.136.0.x < 5     |  |

---

## Saldırı Zinciri

| Aşama | İstek | Amaç |
|-------|--------|------|
| **0** | `GET /openid_connect/cpanelid` | Gerçek sunucu adını keşfet |
| **1** | `POST /login/?login_only=1` (yanlış parola) | Preauth oturum çerezi al |
| **2** | `GET /` + CRLF’li `Authorization: Basic` | Oturum dosyasına `hasroot=1` yaz |
| **3** | `GET /scripts2/listaccts` | Oturumu önbelleğe it (propagasyon) |
| **4** | `GET /cpsessXXXXXXX/json-api/version` | Root erişimini doğrula |

---

## Kurulum

```bash
git clone https://github.com/arsenik/whm-ghost.git
cd whm-ghost
python3 whm_ghost.py -u https://hedef.com:2087







