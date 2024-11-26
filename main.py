import asyncio
import sys
import os
from client import entry
from server import Server

async def main():
    # Initialize server
    Server.server = Server()
    await Server.server.init()
    
    try:
        # Ensure stdout is in line buffering mode
        # sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
        await entry.entry()
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Ensure terminal is in a good state
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('reset')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting due to keyboard interrupt...")