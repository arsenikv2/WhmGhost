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

---

## Kurulum

```bash
git clone https://github.com/arsenik/whm-ghost.git
cd whm-ghost
python3 whm_ghost.py -u https://hedef.com:2087
