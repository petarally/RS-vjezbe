def filtriraj_parne(lista_brojeva):
    return [broj for broj in lista_brojeva if broj % 2 == 0]

lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
parni_brojevi = filtriraj_parne(lista)
print(parni_brojevi)