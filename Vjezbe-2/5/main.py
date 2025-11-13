import shop.proizvodi as proizvodi
import shop.narudzbe as narudzbe

proizvodi_za_dodavanje = [
    {"naziv": "Laptop", "cijena": 5000, "dostupna_kolicina": 10},
    {"naziv": "Monitor", "cijena": 1000, "dostupna_kolicina": 20},
    {"naziv": "Tipkovnica", "cijena": 200, "dostupna_kolicina": 50},
    {"naziv": "Miš", "cijena": 100, "dostupna_kolicina": 100}
]

for podatak in proizvodi_za_dodavanje:
    p = proizvodi.Proizvod(podatak["naziv"], podatak["cijena"], podatak["dostupna_kolicina"])
    proizvodi.dodaj_proizvod(p)

narudzba = narudzbe.napravi_narudzbu(proizvodi_za_dodavanje)
if narudzba:
    narudzba.ispis_narudzbe()

for proizvod in proizvodi.skladiste:
    proizvod.ispis()