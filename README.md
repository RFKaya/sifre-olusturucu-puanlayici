<div align="center">
  <a href="https://istinye.edu.tr">
    <img src="docs/assets/istinye-university-logo.webp" alt="İstinye Üniversitesi" width="180"/>
  </a>

  # Parola Güvenlik Analizörü (Password Security Analyzer)

  ![GitHub](https://img.shields.io/badge/GitHub-Private-red?style=flat-square&logo=github)
  ![Dil](https://img.shields.io/badge/Dil-Python-blue?style=flat-square&logo=python)
  ![Durum](https://img.shields.io/badge/Durum-Devam%20Ediyor-yellow?style=flat-square)
  ![Ders](https://img.shields.io/badge/Ders-BGT006-purple?style=flat-square)
</div>

---

## 🎓 Danışman Bilgisi / Advisor Information

| | |
|---|---|
| **Ad Soyad** | Keyvan Arasteh |
| **GitHub** | [@keyvanarasteh](https://github.com/keyvanarasteh) |
| **E-posta** | [keyvan.arasteh@istinye.edu.tr](mailto:keyvan.arasteh@istinye.edu.tr) |
| **LinkedIn** | [keyvanarasteh](https://www.linkedin.com/in/keyvanarasteh/) |
| **Web Sitesi** | [qline.tech](https://qline.tech) |

---

## 👤 Öğrenci Bilgisi / Student Information

| | |
|---|---|
| **Ad Soyad** | Rauf Fatih Kaya |
| **Öğrenci No** | `2520**1004` |

---

## 📚 Ders Bilgileri / Course Information

| | |
|---|---|
| **Ders Adı** | Sızma Testi (Penetration Testing) |
| **Ders Kodu** | BGT006 |
| **Kredi** | 3 AKTS |
| **Ön Koşullar** | Ağ Temelleri, Linux CLI |
| **Dönem** | 2025-2026 Bahar |

---

## 📋 Proje Özeti / Project Overview

Bu proje, İstinye Üniversitesi Siber Güvenlik Bölümü Bahar 2025-2026 dönemi Sızma Testi (BGT006) dersi final projesi kapsamında geliştirilmiştir. Amacı, kullanıcıların parolalarını kapsamlı testlerden geçiren güvenli bir analiz aracı sunmaktır:
1. **Parola Politikası Denetimi**: Parolanın NIST SP 800-63B standartlarına ve özel tanımlanmış uzunluk/karakter karmaşıklık kurallarına uygunluğunu ölçer.
2. **Güç Puanlama (zxcvbn)**: Dropbox'ın `zxcvbn` algoritmasını kullanarak gerçekçi entropi, sözlük kelimeleri, klavye örüntüleri, leet speak ve tarih eşleşmelerini analiz eder.
3. **Veri İhlali Sorgulama (HIBP)**: `k-Anonymity` prensibini kullanarak kullanıcının şifresini internete göndermeden Have I Been Pwned API üzerinden sızdırılıp sızdırılmadığını sorgular.

---

## 🗂 Repo Yapısı / Repository Structure

```text
final-projeniz/
├── README.md                  # Ana belgeleme (zorunlu)
├── ROADMAP.md                 # Öğrenme ve araştırma yolculuğu (zorunlu)
├── .env.example               # Ortam değişkenleri şablonu (zorunlu)
├── Dockerfile                 # Konteyner tanımı (zorunlu)
├── docker-compose.yml         # Çoklu konteyner yapılandırması (zorunlu)
├── requirements.txt           # Python kütüphaneleri bağımlılıkları
├── docs/
│   ├── modules/               # Modül bazında belgeler
│   ├── research/              # Derinlemesine araştırma notları (docs/research/research_notes.md)
│   └── references/            # Kaynaklar, makaleler, araç linkleri
└── src/                       # Kaynak kod
    ├── main.py                # Giriş noktası
    ├── cli.py                 # Terminal arayüzü (Rich kütüphanesi ile)
    ├── analyzer.py            # Güç ve politika analiz modülü
    ├── breach_checker.py      # HIBP Range API kontrolcü
    └── generator.py           # Güvenli parola üretici (yardımcı modül)
```

---

## 🚀 Kurulum ve Çalıştırma / Getting Started

### Yerel Ortamda Çalıştırma (Python)

1. Depoyu yerel bilgisayarınıza kopyalayın:
   ```bash
   git clone https://github.com/keyvanarasteh/sifre-olusturucu-puanlayici.git
   cd sifre-olusturucu-puanlayici
   ```
2. Sanal ortamı (virtual environment) oluşturun ve aktif edin:
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (CMD):**
     ```cmd
     python -m venv venv
     .\venv\Scripts\activate.bat
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Bağımlılıkları yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. Yapılandırma dosyasını kopyalayın ve düzenleyin:
   ```bash
   cp .env.example .env
   ```
5. Uygulamayı çalıştırın:
   ```bash
   python src/main.py
   ```

### Docker Üzerinde Çalıştırma (Tavsiye Edilen)

1. Docker Compose ile konteyneri derleyin ve etkileşimli modda çalıştırın:
   ```bash
   docker-compose run app
   ```

---

## 📊 Teslim Durumu / Deliverables

| Başlık | Açıklama | Durum |
|--------|----------|:---:|
| **Zorunlu Repo Yapısı** | README, ROADMAP, Dockerfile, env vb. dosyaların tamamlanması | 🟢 |
| **Politika Analizörü** | NIST ve özel parola kurallarının doğrulanması | 🟢 |
| **Güç Puanlama** | zxcvbn entegrasyonu ve entropi ölçümü | 🟢 |
| **İhlal Kontrolü** | k-Anonymity HIBP API entegrasyonu | 🟢 |
| **Kapsamlı Testler** | Otomatik birim testlerinin hazırlanması (`pytest`) | 🟢 |

---

## 📚 Belgelendirme / Documentation

- Tüm modül detayları → [docs/modules/](./docs/modules/)
- Araştırma ve Çıkmaz Sokak Analizleri → [docs/research/research_notes.md](./docs/research/research_notes.md)
