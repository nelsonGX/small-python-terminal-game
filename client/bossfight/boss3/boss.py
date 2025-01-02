import os
import random

from server import Server
from client.assets.reader import get_gui

async def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class get_server_data:
    def __init__(self, session: Server):
        self.session: Server = session
        
    async def init_server(self):
        await self.session.player.calc_stats()

    async def get_gold(self):
        return await self.session.shop.get_owned_currencies()
    async def get_hp(self):
        return await self.session.player.get_hp()
    async def get_hero_id(self):
        return await self.session.player.get_hero_id()
    async def get_level(self):
        return await self.session.player.get_level()
    async def get_player_attack(self):
        return await self.session.player.get_hero_attack()
    async def get_player_defense(self): 
        return await self.session.player.get_hero_defense()
    
    async def get_boss_data(self):
        # boss_id = await self.session.room
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
    # await Server.server.create_saving("test")
    # await Server.server.game_start()
    get_data = get_server_data(Server.server)

    hero_id = await get_data.get_hero_id()
    gold = await get_data.get_gold()
    hp = await get_data.get_hp()
    level = await get_data.get_level()
    atk = await get_data.get_player_attack()
    defense = await get_data.get_player_defense()
    # hero_id = 1
    # gold = 100
    # hp = 100
    # level = 1

    return hero_id, gold, hp, level

async def fight():
    # titls
    boss = await get_gui("boss3")
    you_won = await get_gui("won")

    # get datas
    hero_id, gold, hp, level, atk, defense = await get_all_player_data()
    boss_id, boss_name, boss_hp, boss_atk, boss_def = await get_server_data.get_boss_data(Server.server)

    while hp > 0 and boss_hp > 0:
        who_attack = random.choice(["player", "boss"])

        if who_attack == "player":
            # player attack
            damage = atk
            if damage < 0:
                damage = 0
            boss_hp -= damage

        if who_attack == "boss":
            # boss attack
            damage = boss_atk
            if damage < 0:
                damage = 0
            hp -= damage

        # print the fight
        await clear_screen()
        print(boss)
        print()
        print(f"你的血量: {hp}")
        print(f"Boss的血量: {boss_hp}")
        print()
        print(f"你對Boss造成了 {damage} 點傷害。" if who_attack == "player" else f"Boss對你造成了 {damage} 點傷害。")
        print()
        input("按下Enter繼續...")

    # win the game
    print(you_won)
    exit(0)