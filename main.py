import random
import string

def main():

    #kaç karakterli olsun sorusu
    character = int(input("Kaç karakterli olsun? (1-100):"))
    if (character <= 0 or character > 100):
        print("Karakter uzunluğu 1 ile 100 arasında olmalı.")
        return

    password = ""
    tum_karakterler = string.ascii_letters*2

    #özel karakterler
    specialCharacters = True if input("Özel karakterler olsun mu? (evet/hayır):").lower() == "evet" else False
    if specialCharacters == True: tum_karakterler += string.punctuation

    #sayılar
    numbers = True if input("Sayılar olsun mu? (evet/hayır):").lower() == "evet" else False
    if numbers == True: tum_karakterler += string.digits

    while (len(password) < character): 
        password = password+random.choice(tum_karakterler)
    print(password)

main()