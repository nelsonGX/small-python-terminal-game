import os

from client.assets.reader import get_gui

async def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def fight():
    boss = await get_gui("boss3")
    you_won = await get_gui("won")
    print(you_won)
    exit(0)