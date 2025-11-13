class Kalkulator:
    def __init__(self, a, b):
        self.a = a
        self.b = b      

    def zbroj(self):
        return self.a + self.b

    def oduzimanje(self):
        return self.a - self.b

    def mnozenje(self):
        return self.a * self.b

    def dijeljenje(self):
        if self.b != 0:
            return self.a / self.b
        else:
            return "Dijeljenje s nulom nije dozvoljeno."

    def potenciranje(self):
        return self.a ** self.b

    def korijen(self):
        if self.a >= 0 and self.b >= 0:
            return (self.a ** 0.5, self.b ** 0.5)
        else:
            return "Korijen iz negativnog broja nije definiran u skupu realnih brojeva."