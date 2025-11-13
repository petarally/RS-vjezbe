class Proizvod:
    def __init__(self, naziv, cijena, dostupna_kolicina):
        self.naziv = naziv
        self.cijena = cijena
        self.dostupna_kolicina = dostupna_kolicina

    def ispis(self):
        print(f"Naziv: {self.naziv}, Cijena: {self.cijena}, Dostupna količina: {self.dostupna_kolicina}")   

skladiste = [
    Proizvod("kruh", 2.3, 50),
    Proizvod("mlijeko", 1.5, 30)
]

def dodaj_proizvod(proizvod):
    skladiste.append(proizvod)