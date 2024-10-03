import asyncio
from client.render import render

async def screen():
    while True:
        await render()
        await asyncio.sleep(0.02)