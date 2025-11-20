import asyncio

baza_korisnika = [
    {'korisnicko_ime': 'mirko123', 'email': 'mirko123@gmail.com'},
    {'korisnicko_ime': 'ana_anic', 'email': 'aanic@gmail.com'},
    {'korisnicko_ime': 'maja_0x', 'email': 'majaaaaa@gmail.com'},
    {'korisnicko_ime': 'zdeslav032', 'email': 'deso032@gmail.com'}
]

baza_lozinka = [
    {'korisnicko_ime': 'mirko123', 'lozinka': 'lozinka123'},
    {'korisnicko_ime': 'ana_anic', 'lozinka': 'super_teska_lozinka'},
    {'korisnicko_ime': 'maja_0x', 'lozinka': 's324SDFfdsj234'},
    {'korisnicko_ime': 'zdeslav032', 'lozinka': 'deso123'}
]

async def autorizacija(korisnik_iz_baze, lozinka):
    await asyncio.sleep(2)
    
    korisnicko_ime = korisnik_iz_baze["korisnicko_ime"]
    
    lozinka_iz_baze = None
    for l in baza_lozinka:
        if l["korisnicko_ime"] == korisnicko_ime:
            lozinka_iz_baze = l["lozinka"]
            break
    
    if lozinka_iz_baze == lozinka:
        return f"Korisnik {korisnicko_ime}: Autorizacija uspješna."
    else:
        return f"Korisnik {korisnicko_ime}: Autorizacija neuspješna."

async def autentifikacija(korisnik):
    await asyncio.sleep(3)
    
    korisnicko_ime = korisnik["korisnicko_ime"]
    email = korisnik["email"]
    lozinka = korisnik["lozinka"]
    
    korisnik_iz_baze = None
    for k in baza_korisnika:
        if k["korisnicko_ime"] == korisnicko_ime and k["email"] == email:
            korisnik_iz_baze = k
            break
    
    if korisnik_iz_baze is None:
        return f"Korisnik {korisnicko_ime} nije pronađen."
    
    rezultat = await autorizacija(korisnik_iz_baze, lozinka)
    return rezultat

async def main():
    korisnik1 = {
        "korisnicko_ime": "mirko123",
        "email": "mirko123@gmail.com",
        "lozinka": "lozinka123"
    }
    
    rezultat = await autentifikacija(korisnik1)
    print(rezultat)

if __name__ == "__main__":
    asyncio.run(main())