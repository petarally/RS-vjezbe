class Radnik:
    def __init__(self, ime, pozicija, placa):
        self.ime = ime
        self.pozicija = pozicija
        self.placa = placa      

    def work(self):
        print(f"Radim na poziciji {self.pozicija}") 

class Manager(Radnik):
    def __init__(self, ime, pozicija, placa, department):
        super().__init__(ime, pozicija, placa)
        self.department = department

    def work(self):
        print(f"Radim na poziciji {self.pozicija} u odjelu {self.department}")

    def give_raise(self, radnik, povecanje):
        radnik.placa += povecanje
        print(f"Povećana plaća radnika {radnik.ime} za {povecanje}. Nova plaća je {radnik.placa}")

# Kreiranje instance klase Radnik
radnik1 = Radnik("Ivan", "Programer", 5000)
radnik1.work()      

# Kreiranje instance klase Manager
manager1 = Manager("Ana", "Menadžer", 8000, "IT")
manager1.work()
manager1.give_raise(radnik1, 500)