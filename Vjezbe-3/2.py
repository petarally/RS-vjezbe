import asyncio

async def fetch_users():
    await asyncio.sleep(3)
    users = [
        {"id": 1, "ime": "Ana", "godine": 25},
        {"id": 2, "ime": "Marko", "godine": 30},
        {"id": 3, "ime": "Petra", "godine": 28}
    ]
    print("Korisnici dohvaćeni.")
    return users

async def fetch_products():
    await asyncio.sleep(5)
    products = [
        {"id": 1, "naziv": "Laptop", "cijena": 5000},
        {"id": 2, "naziv": "Miš", "cijena": 100},
        {"id": 3, "naziv": "Tipkovnica", "cijena": 200}
    ]
    print("Proizvodi dohvaćeni.")
    return products

async def main():
    # Kreiranje taskova
    task_users = asyncio.create_task(fetch_users())
    task_products = asyncio.create_task(fetch_products())
    
    # Čekanje rezultata
    users = await task_users
    products = await task_products
    
    print(f"\nKorisnici: {users}")
    print(f"Proizvodi: {products}")

if __name__ == "__main__":
    asyncio.run(main())