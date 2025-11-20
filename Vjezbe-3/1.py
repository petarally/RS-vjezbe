import asyncio

async def fetch_data():
    await asyncio.sleep(3)
    podaci = [broj for broj in range(1, 11)]
    print("Podaci dohvaćeni.")
    return podaci

async def main():
    rezultat = await fetch_data()
    print(f"Vraćeni podaci: {rezultat}")

asyncio.run(main())