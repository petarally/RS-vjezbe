lozinka = input("Unesite lozinku: ")
broj_znakova = len(lozinka)

def provjera_lozinke(lozinka):
    niz = lozinka.lower()
    if "lozinka" in niz or "password" in niz:
        return False, True

    ima_veliko_slovo = any(c.isupper() for c in lozinka)
    ima_broj = any(c.isdigit() for c in lozinka)

    return (ima_veliko_slovo and ima_broj), False

if 8 <= broj_znakova <= 15:
    valid, has_forbidden = provjera_lozinke(lozinka)
    if valid:
        print("Lozinka je jaka!")
    else:
        if has_forbidden:
            print("Lozinka ne smije sadržavati riječi 'lozinka' ili 'password'.")
        else:
            print("Lozinka mora sadržavati barem jedno veliko slovo i jedan broj.")
else:
    print("Lozinka mora sadržavati između 8 i 15 znakova.")