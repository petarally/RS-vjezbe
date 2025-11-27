import cctv
import random
import asyncio

frame_one = cctv.CCTV_frame(1, 10, 20, 30, "Active", "1x", "192.168.1.10")
frame_one.info()

async def simulate_movement(seconds, frame_rate):
    movements = []
    for i in range(0, frame_rate*seconds):
        x = random.uniform(-100, 100)
        y = random.uniform(-100, 100)
        movements.append((x, y))
        await asyncio.sleep(.1)
    return movements

async def main():
    positions = await asyncio.gather(*[simulate_movement(i, 30) for i in range(1, 6)])
    print(positions)
    print((lambda x: sum(len(i) for i in x))(positions))

if __name__ == "__main__":
    asyncio.run(main())