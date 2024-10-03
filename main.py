import asyncio

from client import screen
from server import server

async def main():
    await asyncio.gather(
        server(),
        screen()
    )

if __name__ == '__main__':
    asyncio.run(main())