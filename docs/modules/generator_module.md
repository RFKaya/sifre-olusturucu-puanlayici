# Password Generator Module / Parola Üretici Modülü

## Purpose / Amaç
Kullanıcılara zayıf şifrelerin yerine kullanabilecekleri, tahmin edilmesi zor ve kriptografik olarak güvenli parolalar üretir. İki farklı türde üretim destekler:
1. **Rastgele Güvenli Parola**: Seçilen karakter sınıfları (büyük, küçük, rakam, özel) ve uzunluk kurallarına göre karakter bazlı üretim.
2. **Parola Grubu (Passphrase)**: Diceware mantığıyla, aralarında ayırıcı bulunan akılda kalıcı kelime grupları üretimi.

---

## How It Works / Nasıl Çalışır

### A. Kriptografik Rastgelelik
Sıradan pseudo-random jeneratörler (Python `random` modülü gibi) tahmin edilebilir tohum (seed) değerleri kullanır. Bu modül ise işletim sisteminin sunduğu gerçek rastgelelik kaynağından beslenen **Python `secrets`** kütüphanesini kullanır. Bu sayede üretilen parolalar kriptografik olarak güvenlidir ve tahmin edilemez.

### B. Benzer Karakterlerin Elenmesi (Optional)
Görsel olarak birbirine benzeyen karakterlerin (`l` - `1` - `I` veya `o` - `0` - `O`) karıştırılmasını önlemek amacıyla, talep edilirse bu karakterler havuzdan çıkartılır.

---

## Classes and Methods / Sınıflar ve Metotlar

### `PasswordGenerator` (`src/generator.py`)
- `generate(self, length=16, use_upper=True, use_lower=True, use_digits=True, use_special=True, exclude_similar=True) -> str`: Özelleştirilmiş parametrelere göre güvenli rastgele parola üretir.
- `generate_passphrase(self, num_words=4, separator="-") -> str`: Belirtilen kelime adedine göre kelime bazlı parola grubu üretir.

---

## Usage / Kullanım

```python
from src.generator import PasswordGenerator

generator = PasswordGenerator()

# 16 haneli, benzer karakterler elenmiş rastgele parola
secure_pw = generator.generate(length=16, exclude_similar=True)
print(secure_pw)

# Kelime bazlı parola grubu
passphrase = generator.generate_passphrase(num_words=4, separator="-")
print(passphrase) # Örn: apple-banana-cherry-danger
```
