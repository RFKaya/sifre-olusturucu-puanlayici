import random
import string

character = int(input("Kaç karakterli olsun?:"))
specialCharacters = True if input("Özel karakterler olsun mu? (evet/hayır):").lower() == "evet" else False
numbers = True if input("Sayılar olsun mu? (evet/hayır):").lower() == "evet" else False

password = ""
tum_karakterler = string.ascii_letters
if specialCharacters == True: tum_karakterler += string.punctuation
if numbers == True: tum_karakterler += string.digits

while (len(password) < character): 
    password = password+random.choice(tum_karakterler)

print(password)