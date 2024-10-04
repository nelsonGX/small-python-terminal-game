import asyncio

from client import screen
from server import server

async def main():
    await server.main(),
    await screen.screen()

if __name__ == '__main__':
    asyncio.run(main())