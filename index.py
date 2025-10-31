# Prva linija koda
print("Hello world!")

a = 10
b = 20

print(a, b)

print(type(a))
print(type(b))

bool_1 = True
bool_2 = False

# type hinting
def funkcija(a: int) -> str:
    print(type(a))
    a = str(a)
    print(type(a))
    print("Funkcija je pozvana")

funkcija(5)

# type - debugiranje
# isinstance - provjera tipa
# print(isinstance(a, int)) -> bool

# snakecase je najčešće: prva_varijabla

a = b = c = 5
print(a, b, c)


import math
print(0.1 + 0.2 == 0.3)  # False
close = math.isclose(0.1 + 0.2, 0.3)  # zbog problema sa zaokruživanjem
print(close)


# a is b -> provjera da li su dvije varijable identične (isti objekt u memoriji)

