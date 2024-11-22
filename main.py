import asyncio

from client import entry
from server import Server

async def main():
    Server.server = Server()
    await Server.server.init()
    await entry.entry()

if __name__ == '__main__':
    asyncio.run(main())