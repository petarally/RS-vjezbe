def prvi_i_zadnji(lista):
    if not lista:
        return None, None
    prvi = lista[0]
    zadnji = lista[-1]
    return prvi, zadnji

def min_max(lista):
    if not lista:
        return None, None
    minimum = lista[0]
    maksimum = lista[0]
    for v in lista[1:]:
        if v < minimum:
            minimum = v
        if v > maksimum:
            maksimum = v
    return minimum, maksimum

def presjek(skup1, skup2):
    return skup1.intersection(skup2)

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [5, 10, 20, 50, 100, 11, 250, 50, 80]
print(prvi_i_zadnji(x))  
print(min_max(y))

skup_1 = {1, 2, 3, 4, 5}
skup_2 = {4, 5, 6, 7, 8}
print(presjek(skup_1, skup_2))