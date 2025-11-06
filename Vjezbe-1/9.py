def ukloni_duplikate(lista):
    skup = set()
    nova_lista = []
    for element in lista:
        if element not in skup:
            skup.add(element)
            nova_lista.append(element)
    return nova_lista

ulazna_lista = [1, 2, 2, 3, 4, 4, 5]
izlazna_lista = ukloni_duplikate(ulazna_lista)
print(izlazna_lista) 