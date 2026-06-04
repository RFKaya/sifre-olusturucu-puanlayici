# Password Analyzer Module / Parola Analizör Modülü

## Purpose / Amaç
Bu modül, kullanıcı tarafından girilen parolanın güvenliğini iki yönden analiz eder:
1. **Politika Analizi**: Belirlenen minimum uzunluk, büyük/küçük harf, rakam, özel karakter ve yasaklı kelime listelerine uyumluluk.
2. **Güç Puanlama (zxcvbn)**: Dropbox'ın örüntü tanıma motoruyla şifrenin karmaşıklığını derecelendirme (0-4).
3. **Veri İhlali Denetimi (Breach Checker)**: Have I Been Pwned API'si üzerinden k-Anonymity (SHA-1) protokolüyle ihlal durumunu sorgulama.

---

## How It Works / Nasıl Çalışır

### A. Politika Denetimi
Parola karakter dizisi analiz edilerek, `.env` dosyasındaki kurallara göre filtrelenir. Eğer parolanın içinde `CUSTOM_BLACKLIST_WORDS` tanımlı kelimelerden biri geçiyorsa, kural ihlali sayılır ve geçersiz kabul edilir.

### B. zxcvbn ile Güç Puanlama
Geleneksel karakter havuzu formüllerinin aksine, şifrenin içindeki anlamlı kelimeler (sözlük kelimeleri), tarih desenleri, klavye sıralı dizilimleri (`qwerty`) ve tekrarlayan yapılar taranarak bir kırma tahmini (guesses) hesaplanır.

### C. k-Anonymity Sızıntı Kontrolü
Parolanın SHA-1 özeti çıkarılır. Gizliliği tehlikeye atmamak adına, sadece ilk 5 karakteri Have I Been Pwned sunucularına gönderilir. Geri dönen olası sızıntı listesindeki son 35 karakter yerel olarak karşılaştırılarak sızma adedi ve tehlike derecesi saptanır.

---

## Classes and Methods / Sınıflar ve Metotlar

### 1. `PasswordAnalyzer` (`src/analyzer.py`)
- `__init__(self)`: `.env` yapılandırmasını yükler.
- `check_policy(self, password: str) -> dict`: Parolayı uzunluk ve karakter kurallarına göre denetler.
- `calculate_entropy(self, password: str) -> float`: Matematiksel entropiyi hesaplar ($H = L \log_2 R$).
- `analyze_strength(self, password: str) -> dict`: `zxcvbn` analiziyle tahmin zorluğunu ve önerileri hesaplar.

### 2. `BreachChecker` (`src/breach_checker.py`)
- `check_password_breaches(self, password: str) -> dict`: k-Anonymity kullanarak şifrenin sızıntı geçmişini sorgular.

---

## Usage / Kullanım

```python
from src.analyzer import PasswordAnalyzer
from src.breach_checker import BreachChecker

analyzer = PasswordAnalyzer()
checker = BreachChecker()

password = "MySecurePassword123!"

# Politika Kontrolü
policy_res = analyzer.check_policy(password)
print(policy_res["is_compliant"]) # True veya False

# Güç Puanlama
strength_res = analyzer.analyze_strength(password)
print(strength_res["score"]) # 0 ile 4 arası değer

# Sızıntı Sorgusu
breach_res = checker.check_password_breaches(password)
print(breach_res["count"]) # Sızma adedi
```

---

## Known Limitations / Bilinen Kısıtlamalar
- İnternet bağlantısı koptuğunda HIBP API çalışmaz ve sızıntı kontrolü atlanır (çevrimdışı mod uyarısı verir).
- Çok uzun şifrelerde (örneğin 100+ karakter) `zxcvbn` analizi işlemciyi kısa süreliğine yorabilir.
