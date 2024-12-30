import asyncio
import sys
import os
from client import entry
from server import Server

async def main():
    # Initialize server
    server = Server()
    await server.init()

    await entry.entry()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")