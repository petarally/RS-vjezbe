rjecnik = {"ime": "Ivan", "prezime": "Ivić", "dob": 25}

def obrni_rjecnik(rjecnik):
    novi_rjecnik = {}
    for kljuc, vrijednost in rjecnik.items():
        novi_rjecnik[vrijednost] = kljuc
    return novi_rjecnik

print(obrni_rjecnik(rjecnik))