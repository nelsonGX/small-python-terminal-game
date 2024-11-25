import asyncio
import sys

from client import entry
from server import Server

async def main():
    Server.server = Server()
    await Server.server.init()
    try:
        await entry.entry()
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt...")