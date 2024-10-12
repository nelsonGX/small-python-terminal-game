import asyncio

from client import screen
from server import Server

async def main():
    Server.server = Server()
    await Server.server.init()
    await screen.screen()

if __name__ == '__main__':
    asyncio.run(main())