import asyncio

from client.bossfight.boss1.diceroller import Dice3D
from client.assets.reader import get_gui
from server import Server

async def get_boss_data():
    # TODO @andy
    # dummy data
    boss_id = 1
    boss_name = "Goblin"
    boss_hp = 100
    boss_atk = 10
    boss_def = 5
    return boss_id, boss_name, boss_hp, boss_atk, boss_def

async def fight():
    # start the game
    boss_id, boss_name, boss_hp, boss_atk, boss_def = await get_boss_data()

# testing
if __name__ == "__main__":
    asyncio.run(fight())