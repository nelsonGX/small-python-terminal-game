import asyncio
from render import render

async def screen():
    while True:
        await render(100, 0)
        await asyncio.sleep(0.02)

# testing
asyncio.run(screen())