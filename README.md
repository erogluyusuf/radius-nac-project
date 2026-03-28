#  Network Access Control (NAC) Sistemi

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![FreeRADIUS](https://img.shields.io/badge/FreeRADIUS-3.2-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

Bu proje, RADIUS protokolünü kullanarak temel düzeyde çalışan bir **Network Access Control (NAC)** sistemidir.Kimlik doğrulama (Authentication), yetkilendirme (Authorization) ve hesap yönetimi (Accounting) — yani **AAA mimarisi** — üzerine inşa edilmiştir.

##  Proje Mimarisi
 
Sistem, mikroservis yaklaşımıyla Docker üzerinde koşturulmaktadır ve tüm bileşenler izole bir Docker ağı üzerinden haberleşir:

- **FreeRADIUS 3.2:** Sistemin kalbi. Kimlik doğrulama ve hesap yönetimi taleplerini karşılar, `rlm_rest` modülü ile FastAPI'ye yönlendirir.
- **FastAPI (Python 3.13):** Karar mekanizması (Policy Engine). RADIUS'tan gelen HTTP POST isteklerini işler ve yetkilendirme politikalarını (VLAN vs.) belirler.
- **PostgreSQL 18:** Kullanıcı kimlik bilgileri, MAC adresleri ve geçmiş oturum (radacct) kayıtlarının kalıcı olarak tutulduğu ilişkisel veritabanı.
- **Redis 8:** Aktif oturumların hızlı takibi ve başarısız giriş denemelerine karşı **rate-limiting** uygulanması için kullanılan bellek içi veri yapısı.

##  Kurulum ve Çalıştırma

Sistemi ayağa kaldırmak için bilgisayarınızda **Docker** ve **Docker Compose** yüklü olmalıdır.

**1. Repoyu Klonlayın:**
```bash
git clone https://github.com/erogluyusuf/radius-nac-project.git
cd radius-nac-project
```

**2. Çevresel Değişkenleri (Environment Variables) Ayarlayın:**
Proje kök dizinindeki örnek env dosyasını kopyalayarak kendi şifrelerinizi belirleyin.
```bash
cp .env.example .env
```

**3. Konteynerleri Başlatın:**
```bash
docker-compose up -d --build
```
*(Bu komut PostgreSQL, Redis, FastAPI ve FreeRADIUS servislerini ayağa kaldıracaktır.)*

##  Sistemi Test Etme

Sistemin çalıştığını doğrulamak için FreeRADIUS konteyneri içerisinden test araçlarını (`radtest` ve `radclient`) kullanabilirsiniz.

**1. PAP/CHAP (Kullanıcı Adı/Şifre) Testi:**
```bash
docker exec -it freeradius radtest kullaniciadi sifre localhost 0 testing123
```

**2. MAB (MAC Authentication Bypass) Testi:**
(802.1X desteklemeyen yazıcı/telefon gibi cihazlar için)
```bash
echo "User-Name=AA:BB:CC:DD:EE:FF, Calling-Station-Id=AA-BB-CC-DD-EE-FF" | docker exec -i freeradius radclient -x localhost auth testing123
```

##  API Endpoint'leri (FastAPI)

Policy Engine, `http://localhost:8000` adresi üzerinden `rlm_rest` modülü ile haberleşir:

| Metot | Endpoint | İşlev |
| :--- | :--- | :--- |
| **POST** | `/auth` | Kullanıcı veya MAC adresi doğrulaması (Authentication) |
| **POST** | `/authorize` | Dinamik VLAN ve politika ataması (Authorization) |
| **POST** | `/accounting` | RADIUS oturum verilerini kaydetme (Accounting) |
| **GET** | `/sessions/active`| Redis üzerindeki aktif oturumları listeleme |

##  Güvenlik Önlemleri
- Başarısız kimlik doğrulama denemeleri **Redis üzerinden rate-limiting** ile sınırlandırılmıştır.
- Hassas veriler (veritabanı şifreleri, RADIUS secret) `.env` dosyası ile izole edilmiştir.
- Kullanıcı şifreleri veritabanında düz metin (plaintext) olarak değil, güvenli hash algoritmalarıyla saklanmaktadır.
