import asyncio

async def secure_data(osjetljivi_podaci):
    await asyncio.sleep(3)  
    
    enkriptirani_podaci = {
        'prezime': osjetljivi_podaci['prezime'],
        'broj_kartice': hash(osjetljivi_podaci['broj_kartice']),
        'CVV': hash(osjetljivi_podaci['CVV'])
    }
    
    return enkriptirani_podaci

async def main():
    osjetljivi_podaci_lista = [
        {'prezime': 'Horvat', 'broj_kartice': '1234-5678-9012-3456', 'CVV': '123'},
        {'prezime': 'Kovač', 'broj_kartice': '9876-5432-1098-7654', 'CVV': '456'},
        {'prezime': 'Novak', 'broj_kartice': '1111-2222-3333-4444', 'CVV': '789'}
    ]
    
    print("Originalni podaci:")
    for podaci in osjetljivi_podaci_lista:
        print(podaci)
    print()
    
    zadaci = [asyncio.create_task(secure_data(podaci)) for podaci in osjetljivi_podaci_lista]
    
    enkriptirani_rezultati = await asyncio.gather(*zadaci)
    
    print("Enkriptirani podaci:")
    for rezultat in enkriptirani_rezultati:
        print(rezultat)

if __name__ == "__main__":
    asyncio.run(main())