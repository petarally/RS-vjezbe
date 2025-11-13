from datetime import datetime
class Automobil:
    def __init__(self, marka, model, godina_proizvodnje, kilometraža):
        self.marka = marka
        self.model = model
        self.godina_proizvodnje = godina_proizvodnje
        self.kilometraža = kilometraža

    def ispis(self):
        print(f"Marka: {self.marka}")
        print(f"Model: {self.model}")
        print(f"Godina proizvodnje: {self.godina_proizvodnje}")
        print(f"Kilometraža: {self.kilometraža} km")

    def starost(self):
        trenutna_godina = datetime.now().year
        starost_automobila = trenutna_godina - self.godina_proizvodnje
        print(f"Automobil je star {starost_automobila} godina.")