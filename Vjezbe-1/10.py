tekst = "Python je programski jezik koji je jednostavan za učenje i korištenje. Python je vrlo popularan."

def brojanje_riječi(tekst):
    riječi = tekst.split()
    frekvencije = {}
    for r in riječi:
        frekvencije[r] = frekvencije.get(r, 0) + 1
    return frekvencije

print(brojanje_riječi(tekst))