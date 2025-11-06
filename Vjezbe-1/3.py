import random

x = int(input("Unesite broj između 1 i 100: "))
y = random.randint(1, 100)
broj_je_pogoden = False
broj_pokusaja = 0

while not broj_je_pogoden:
    if x < y:
        print("Veće")
        x = int(input())
    elif x > y:
        print("Manje")
        x = int(input())
    else:
        print("Pogodak")
        broj_je_pogoden = True
    broj_pokusaja += 1

print("Bravo, pogodio si u {} pokušaja".format(broj_pokusaja))