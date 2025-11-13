class Narudzba:
    def __init__(self, naruceni_proizvodi, ukupna_cijena):
        self.naruceni_proizvodi = naruceni_proizvodi
        self.ukupna_cijena = ukupna_cijena

    def ispis_narudzbe(self):
        proizvodi_str = ", ".join([f"{p['naziv']} x {p['narucena_kolicina']}" for p in self.naruceni_proizvodi])
        print(f"Naručeni proizvodi: {proizvodi_str}, Ukupna cijena: {self.ukupna_cijena} eur")


def napravi_narudzbu(naruceni_proizvodi):
    if not isinstance(naruceni_proizvodi, list) or len(naruceni_proizvodi) == 0:
        print("Naruceni proizvodi mora biti ne-prazna lista!")
        return None

    for proizvod in naruceni_proizvodi:
        if not isinstance(proizvod, dict):
            print("Svaki element u listi mora biti rječnik!")
            return None
        if not all(key in proizvod for key in ["naziv", "cijena", "narucena_kolicina"]):
            print("Rječnik mora sadržavati ključeve naziv, cijena i narucena_kolicina!")
            return None

    ukupna_cijena = sum(proizvod["cijena"] * proizvod["narucena_kolicina"] for proizvod in naruceni_proizvodi)

    for proizvod in naruceni_proizvodi:
        naziv = proizvod["naziv"]
        kolicina = proizvod["narucena_kolicina"]
        from shop.proizvodi import skladiste
        dostupni_proizvod = next((p for p in skladiste if p.naziv == naziv), None)
        if dostupni_proizvod is None or dostupni_proizvod.dostupna_kolicina < kolicina:
            print(f"Proizvod {naziv} nije dostupan!")
            return None

    return Narudzba(naruceni_proizvodi, ukupna_cijena)