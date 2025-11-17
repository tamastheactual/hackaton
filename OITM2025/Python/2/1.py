import asyncio

async def open_valve():
    await asyncio.sleep(1)
    return 42

async def start_engine():
    task = asyncio.create_task(open_valve())
    return await task

print(asyncio.run(start_engine()))
