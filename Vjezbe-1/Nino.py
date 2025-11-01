from podatci import tablica_brojeva
import re

def validiraj_broj_telefona(broj_telefona: str) -> dict:
    validacija = {}
    # Broj telefona sadrži samo znamenke
    if isinstance(broj_telefona, str):
        broj_telefona = re.sub(r'\D+', '', broj_telefona)
    # Provjera i uklanjanje pozivnog broja za Hrvatsku
    if(broj_telefona[0:3] == '385'):
        broj_telefona = broj_telefona[3:]
    elif(broj_telefona[0:5] == '00385'):
        broj_telefona = broj_telefona[5:]
    # Provjera lokalnog broja telefona
    validacija = usporedba_s_bazom(broj_telefona, tablica_brojeva)
    return validacija


def usporedba_s_bazom(broj_telefona: str, baza: list) -> dict:
    rezultat = {}
    if(broj_telefona[:2] == '01'):
        broj_ostatak = broj_telefona[2:]
        index = baza.index(next(filter(lambda d: d['pozivni_broj'] == '01', baza), None))
        rezultat["pozivni_broj"] = '01'
        rezultat["broj_ostatak"] = broj_ostatak
        rezultat["vrsta"] = baza[index]["vrsta"]
        rezultat["mjesto"] = baza[index]["mjesto"]
        rezultat["operater"] = None
        if(len(broj_ostatak) == 6 or len(broj_ostatak) == 7):
            rezultat["validan"] = True
        else:
            rezultat["validan"] = False
    elif(broj_telefona[:4] == '0800'):
        broj_ostatak = broj_telefona[4:]
        index = baza.index(next(filter(lambda d: d['pozivni_broj'] == '0800', baza), None))
        rezultat["pozivni_broj"] = '0800'
        rezultat["broj_ostatak"] = broj_ostatak
        rezultat["vrsta"] = baza[index]["vrsta"]
        rezultat["mjesto"] = baza[index]["mjesto"]
        rezultat["operater"] = None
        if(len(broj_ostatak) == 6):
            rezultat["validan"] = True
        else:
            rezultat["validan"] = False
    else:
        pozivni_broj = broj_telefona[:3]
        broj_ostatak = broj_telefona[3:]
        index = baza.index(next(filter(lambda d: d['pozivni_broj'] == pozivni_broj, baza), None))
        rezultat["pozivni_broj"] = pozivni_broj
        rezultat["broj_ostatak"] = broj_ostatak
        rezultat["vrsta"] = baza[index]["vrsta"]
        rezultat["mjesto"] = baza[index]["mjesto"]
        rezultat["operater"] = None
        if(index is not None and len(broj_ostatak) == 6 or len(broj_ostatak) == 7):
            rezultat["validan"] = True
        else:
            rezultat["validan"] = False
    return rezultat  


# TODO:
# - Problem s 098 i 099 pozivnim brojevima
# - Problem s upisom brojeva bez 0 (1 umjesto 01)