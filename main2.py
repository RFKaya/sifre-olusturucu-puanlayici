import time
import string

point = 0
olanlar = []
olmayanlar = []
password = input("Şifrenizi giriniz:")

time.sleep(1)
print("Şifreniz inceleniyor...")
time.sleep(2)

if (len(password) < 8):
    olmayanlar.append("Şifre daha uzun olmalıdır ❌")
elif (len(password) < 16):
    point += 10
    olmayanlar.append("Şifre biraz daha uzun olmalıdır ❌")
else:
    point += 20
    olanlar.append("Şifre yeterli uzunlukta ✅")

if password.upper() == password:
    olmayanlar.append("Şifrede hiç küçük harf yok ❌")
else:
    point += 15
    olanlar.append("Şifrede küçük harf var ✅")

if password.lower() == password:
    olmayanlar.append("Şifrede hiç büyük harf yok ❌")
else:
    point += 20
    olanlar.append("Şifrede büyük harf var ✅")

if any(karakter.isdigit() for karakter in password):
    point += 20
    olanlar.append("Şifrede sayı var ✅")
else:
    olmayanlar.append("Şifrede hiç sayı yok ❌")

if any(c in string.punctuation for c in password):
    puan += 25
    olanlar.append("Şifrede özel karakter var ✅")
else: 
    olmayanlar.append("Şifrede özel karakter yok ❌")

for i in olanlar:
    print(i)
    time.sleep(1)

for i in olmayanlar:
    print(i)
    time.sleep(1)

print("Puanınız (100 üzerinden):", point)