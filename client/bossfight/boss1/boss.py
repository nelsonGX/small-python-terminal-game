import asyncio
import os

from client.bossfight.boss1.diceroller import Dice3D
from client.assets.reader import get_gui
from server import Server

class get_server_data:
    def __init__(self, session: Server):
        self.session: Server = session

    async def get_gold(self):
        return await self.session.shop.get_owned_currencies()
    async def get_hp(self):
        return await self.session.player.get_hp()
    async def get_hero_id(self):
        return await self.session.player.get_hero_id()
    async def get_level(self):
        return await self.session.player.get_level()
    
    async def get_boss_data(self):
        # boss_id = await self.session.room..get_boss_id()
        # boss_name = await self.session.boss.get_boss_name()
        # boss_hp = await self.session.boss.get_boss_hp()
        # boss_atk = await self.session.boss.get_boss_atk()
        # boss_def = await self.session.boss.get_boss_def()
        boss_id = 1
        boss_name = "Boss"
        boss_hp = 100
        boss_atk = 10
        boss_def = 5
        return boss_id, boss_name, boss_hp, boss_atk, boss_def

async def get_all_player_data():
    get_data = get_server_data(Server.server)

    hero_id = await get_data.get_hero_id()
    gold = await get_data.get_gold()
    hp = await get_data.get_hp()
    level = await get_data.get_level()
    # hero_id = 1
    # gold = 100
    # hp = 100
    # level = 1

    return hero_id, gold, hp, level

async def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def fight():
    # start the game
    await clear_screen()

    # get data
    boss_id, boss_name, boss_hp, boss_atk, boss_def = await get_server_data.get_boss_data(Server.server)
    hero_id, gold, hp, level = await get_all_player_data()

    boss = await get_gui("boss1")
    boss_fight = await get_gui("boss1_2")
    boss_dead = await get_gui("boss1_3")
    player_dead = await get_gui("dead")

    # show the boss
    print(boss)
    print(boss_name)
    print(f"HP: {boss_hp}")
    print(f"ATK: {boss_atk}")
    print(f"DEF: {boss_def}")
    print()
    print("Player")
    print(f"HP: {hp}")
    print(f"Level: {level}")
    print()
    print("你必須跟他擲骰子比大小！")

    input("Press Enter to start the fight...")

    while True:
        # roll the dice
        dice = Dice3D()
        boss_roll = dice.roll()
        await clear_screen()
        print(boss)
        print()
        print(f"{boss_name} rolled {boss_roll}!")
        print()
        input("Press Enter to roll the dice...")
        player_roll = dice.roll()

        await clear_screen()
        if player_roll > boss_roll:
            boss_hp -= 15

            print(boss)
            await asyncio.sleep(0.5)
            await clear_screen()
            print(boss_dead)
            print(boss_name)
            print(f"HP: {boss_hp}")
            print(f"ATK: {boss_atk}")
            print(f"DEF: {boss_def}")
            print()
            print("Player")
            print(f"HP: {hp}")
            print(f"Level: {level}")
            print()
            print("Player wins!")

        elif player_roll < boss_roll:
            hp -= boss_atk

            print(boss)
            await asyncio.sleep(0.5)
            await clear_screen()
            print(boss_fight)
            print(boss_name)
            print(f"HP: {boss_hp}")
            print(f"ATK: {boss_atk}")
            print(f"DEF: {boss_def}")
            print()
            print("Player")
            print(f"HP: {hp}")
            print(f"Level: {level}")
            print()
            print(f"{boss_name} wins!")
        elif player_roll == boss_roll:
            print("It's a draw!")
            continue

        # check if player is dead
        if hp <= 0:
            print(player_dead)
            print()
            print("You are dead!")
            input("Press Enter to exit...")
            return False

        # check if boss is dead
        if boss_hp <= 0:
            print(f"{boss_name} is dead!")
            input("Press Enter to exit...")
            return True

        # pause
        print()
        input("Press Enter to continue...")

# testing
if __name__ == "__main__":
    asyncio.run(fight())