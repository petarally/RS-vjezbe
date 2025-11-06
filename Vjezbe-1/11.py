lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def grupiraj_po_paritetu(lista):
    rezultat = {'parni': [], 'neparni': []}
    for broj in lista:
        if broj % 2 == 0:
            rezultat['parni'].append(broj)
        else:
            rezultat['neparni'].append(broj)
    return rezultat

print(grupiraj_po_paritetu(lista))