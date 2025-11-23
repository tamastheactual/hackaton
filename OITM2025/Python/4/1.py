import asyncio


async def big_engine():
    print('Starting big engine...')
    await asyncio.sleep(5)
    print("Big engine is ready.")
    return 0


async def small_engine():
    print("Starting small engine...")
    await asyncio.sleep(1)
    print("Small engine is ready.")
    return 0


async def main():
    await asyncio.gather(big_engine(), small_engine())


if __name__ == "__main__":
    asyncio.run(main())
