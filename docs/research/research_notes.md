# Research Notes / Araştırma Notları

> **Modül / Konu**: Parola Güvenlik Analizörü (Password Security Analyzer)  
> **Tarih / Date**: 2026-06-04  
> **Ders / Course**: BGT006 Sızma Testi  

---

## 1. Ne Araştırıyorum / What I'm Investigating
Bu araştırmanın amacı, modern ve güvenli bir parola analiz ve puanlama sisteminin arkasındaki teorik altyapıyı oluşturmaktır. Çalışma üç ana odağa ayrılmıştır:
1. **Parola Gücü ve Entropi**: Geleneksel karakter sınıfları (büyük-küçük harf, rakam vb.) yerine neden `zxcvbn` gibi örüntü tabanlı kütüphanelerin tercih edilmesi gerektiği.
2. **Güvenli Sızıntı Kontrolü (k-Anonymity)**: Kullanıcının parolasını internete göndermeden, Have I Been Pwned (HIBP) veritabanında nasıl sorgulayabileceğimiz.
3. **NIST SP 800-63B Kriterleri**: Modern siber güvenlik dünyasında kabul gören en güncel parola politikası standartları.

---

## 2. Bulunan Kaynaklar / Resources Found

- [NIST SP 800-63B Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html) — Modern parola politikası önerileri (karmaşıklık kuralları yerine sızıntı kontrolü ve uzunluğa odaklanma).
- [zxcvbn GitHub Repository](https://github.com/dropbox/zxcvbn) — Dropbox tarafından geliştirilen, sözlükler, klavye desenleri ve tarih analizleri kullanan parola güç tahmin edicisi.
- [Have I Been Pwned API Docs](https://haveibeenpwned.com/API/v3) — k-Anonymity prensibi ile çalışan Range API.
- [Cloudflare: Password Leak Checking with k-Anonymity](https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/) — k-Anonymity teorisi ve gizliliğin korunması.

---

## 3. Temel Bulgular / Key Findings

### A. Geleneksel Entropi vs. zxcvbn
- **Geleneksel Entropi ($H = L \log_2 R$)**: Karakter kümesi boyutu ($R$) ve parola uzunluğu ($L$) üzerinden hesaplama yapar. Ancak `P@$$w0rd123!` gibi sık kullanılan şablonlar bu formülde yüksek puan alırken, sözlük tabanlı ve tahmin edilmesi çok kolay parolalardır.
- **zxcvbn Mantığı**: Parolayı alt dizelere böler. Sözlükler (isimler, popüler kelimeler, sızdırılmış şifreler), klavye dizilimleri (horizontal/vertical/dvorak), tekrarlayan karakterler (`aaaa`), ardışık diziler (`12345`) ve tarihler (`1998`) üzerinden eşleştirme yapar. En düşük entropiyi veren kombinasyon üzerinden gerçekçi bir tahmin yürütür.

### B. HIBP Range API ve k-Anonymity Çalışma Prensibi
Kullanıcı parolasının gizliliğini korumak için şu protokol izlenir:
1. Parolanın **SHA-1** özeti (hash) hesaplanır. Örnek: `P@ssword123` -> `58633a276189914755a6d092040b1df639c0b1ef`.
2. Hash değerinin **ilk 5 karakteri** (prefix) alınır: `58633`.
3. Sadece bu 5 karakter API'ye gönderilir: `GET https://api.pwnedpasswords.com/range/58633`
4. API, bu ön ek ile başlayan binlerce sızdırılmış parolanın hash değerlerinin geri kalan 35 karakterini (suffix) ve sızma sayılarını içeren bir liste döner:
   ```text
   A276189914755A6D092040B1DF639C0B1EF:4820
   B812F...
   ```
5. İstemci (bizim kodumuz), dönen listeyi yerel olarak tarar. Eğer bizim hash'in son 35 karakteri (`a276189914755a6d092040b1df639c0b1ef`) eşleşirse, parolanın sızdırıldığını anlarız ve sızma sayısını kullanıcıya gösteririz. Bu sayede parola asla bilgisayarımızdan dışarı çıkmaz.

---

## 4. Çıkmaz Sokaklar / Dead Ends

- **Tüm SHA-1 Hash'ini API'ye Göndermek**: Doğrudan tüm hash sorgulaması yapan API uç noktalarını araştırdık. Ancak bu yöntem ağ dinleme saldırılarına (MITM) maruz kalma riskini ve sunucu tarafında kayıt tutulma olasılığını barındırır. Projede kesinlikle **k-Anonymity Range API** kullanılmalıdır.
- **Statik Kelime Listesiyle Yerel Sızıntı Kontrolü**: Rockyou.txt gibi dosyaları konteyner içine gömmeyi düşündük. Ancak bu işlem Docker imaj boyutunu GB seviyelerine çıkarır ve güncel sızıntıları yakalayamaz. HIBP Range API bu sorunu dinamik ve verimli şekilde çözer.

---

## 5. Kalan Sorular / Questions Remaining
- [x] HIBP API istek limiti nedir? (Range API için herhangi bir API Key gerekmez ve istek limiti yok denecek kadar yüksektir).
- [x] Çevrimdışı (offline) mod desteği olmalı mı? Evet, internet bağlantısı olmadığında HIBP sorgusunu atlayıp sadece zxcvbn ve yerel analizleri yapacak bir mekanizma kurulmalıdır.

---

## 6. 50 Adımlık Çözümleme / 50-Step Breakdown

Burada, parola analizi ve yönetimi konusunu en temelden başlayarak 50 küçük adıma böldük:

### 1-10: Temel Kavramlar & Kriptografi
1. Parola nedir ve neden kimlik doğrulamada kritik öneme sahiptir?
2. Kriptografik özet fonksiyonu (Hash) nedir?
3. MD5, SHA-1, SHA-256 arasındaki farklar nelerdir?
4. Neden parolalar açık metin (plaintext) olarak saklanmamalıdır?
5. Tuzlama (Salt) nedir ve gökkuşağı tablolarını (Rainbow Tables) nasıl engeller?
6. BCRYPT ve PBKDF2 gibi yavaş hash algoritmalarının önemi nedir?
7. Brute-force (kaba kuvvet) saldırısı nedir?
8. Sözlük (Dictionary) saldırısı nedir?
9. Kimlik bilgisi doldurma (Credential Stuffing) nedir?
10. Sosyal mühendislik tabanlı parola tahminleri nasıl yapılır?

### 11-20: Güvenlik Politikaları & Standartlar
11. Geleneksel parola karmaşıklık kuralları nelerdir?
12. NIST SP 800-63B standardı nedir?
13. NIST neden karmaşık karakter kurallarını artık önermiyor?
14. Parola uzunluğu (length) neden karakter havuzundan (R) daha etkilidir?
15. Periyodik parola değiştirme politikalarının zafiyetleri nelerdir?
16. "Bilinen sızdırılmış parolaların kara listeye alınması" standardı nedir?
17. HIBP (Have I Been Pwned) veritabanı nedir ve kim tarafından yönetilir?
18. Troy Hunt kimdir?
19. Bir veri sızıntısının (Data Breach) anatomisi nasıldır?
20. Password Manager (Parola Yöneticisi) araçları neden önerilir?

### 21-30: Matematiksel Hesaplama & Algoritmalar
21. Parola Entropisi bit cinsinden nasıl hesaplanır? ($H = L \log_2 R$)
22. Entropi hesaplamasında kullanılan karakter havuzları nasıl tanımlanır?
23. Şifre gücü tahmininde Shannon Entropisi kullanılabilir mi?
24. `zxcvbn` kütüphanesi nedir ve nasıl çalışır?
25. `zxcvbn` hangi yerleşik sözlükleri barındırır (isimler, soyisimler, popüler kelimeler)?
26. Klavye örüntüsü (keyboard walk) tespiti algoritması nasıl çalışır?
27. L33t speak (ör. `a` yerine `@` veya `4`) dönüşümleri nasıl tespit edilir?
28. Tarih ve yıl örüntüleri (ör. `1990`, `2024`) parola gücünü nasıl etkiler?
29. Tekrarlayan ve ardışık karakterlerin tespiti nasıl yapılır?
30. Tahmin adımı (Guesses) kavramı nedir?

### 31-40: HIBP Range API ve Gizlilik (k-Anonymity)
31. k-Anonymity teorik olarak ne anlama gelir?
32. Parola sızıntısı sorgularken gizlilik neden en büyük endişedir?
33. HIBP Range API nasıl çağrılır?
34. API neden parolanın kendisini veya tüm hash'ini kabul etmez?
35. Neden tam olarak ilk 5 SHA-1 karakteri gönderilir?
36. 5 karakterlik ön ek (prefix) kaç olası kombinasyon üretir? ($16^5 = 1,048,576$)
37. Range API'nin döndüğü veri yapısı nasıldır?
38. Geriye kalan 35 karakterlik hash kısmı (suffix) nasıl karşılaştırılır?
39. API'den dönen listede arama yaparken performans nasıl optimize edilir?
40. API bağlantısı koptuğunda veya internet yokken sistem nasıl davranmalıdır?

### 41-50: Uygulama & Entegrasyon
41. Python'da CLI uygulamaları için `rich` kütüphanesi nasıl kurulur ve yapılandırılır?
42. Terminal üzerinden parola girilirken karakterlerin gizlenmesi (masking) nasıl sağlanır?
43. Parola gücü derecelendirme aralıkları (0 - 4 arası) nasıl görselleştirilir?
44. Dockerfile ile Python CLI uygulaması nasıl konteyner haline getirilir?
45. Docker Compose ile terminal etkileşimli mod nasıl yapılandırılır?
46. `.env` dosyası üzerinden politika kuralları (min_length, custom_words) nasıl okunur?
47. `pytest` ile parola analizörünün doğruluğu nasıl test edilir?
48. HIBP API bağlantısı Mock'lanarak birim testleri nasıl yazılır?
49. Kod kalitesi ve güvenlik zafiyetleri için statik kod analizi (linting) nasıl yapılır?
50. Projenin teslimi için eğitmen collaborator olarak nasıl davet edilir?
