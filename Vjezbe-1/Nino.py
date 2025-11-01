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
    if broj_telefona.startswith('0') == False:
        broj_telefona = '0' + broj_telefona
    if broj_telefona[:4] == '0800':
        pozivni_broj = '0800'
        validne_duljine = {6}
    elif broj_telefona[:2] == '01':
        pozivni_broj = '01'
        validne_duljine = {6, 7}
    else:
        pozivni_broj = broj_telefona[:3]
        validne_duljine = {6, 7}
    
    broj_ostatak = broj_telefona[len(pozivni_broj):]
    zapis_brojevi = next(filter(lambda d: pozivni_broj in (d['pozivni_broj'] if isinstance(d['pozivni_broj'], list) else [d['pozivni_broj']]), baza), None)

    return {
        "pozivni_broj": pozivni_broj,
        "broj_ostatak": broj_ostatak,
        "vrsta": zapis_brojevi["vrsta"] if zapis_brojevi else None,
        "mjesto": zapis_brojevi["mjesto"] if zapis_brojevi else None,
        "operater": None,
        "validan": len(broj_ostatak) in validne_duljine
    } 