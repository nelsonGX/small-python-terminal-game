import asyncio
from client.render import render

async def screen():
    while True:
        await render(100, 0)
        await asyncio.sleep(0.02)