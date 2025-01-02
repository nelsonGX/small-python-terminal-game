import random
import os

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

async def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def get_all_player_data():
    get_data = get_server_data(Server.server)

    # hero_id = await get_data.get_hero_id()
    # gold = await get_data.get_gold()
    # hp = await get_data.get_hp()
    # level = await get_data.get_level()
    hero_id = 1
    gold = 100
    hp = 100
    level = 1

    return hero_id, gold, hp, level

async def guess_riddle(question, answer, reason="", boss_atk=10):
    print("\n猜謎遊戲！")
    print(question)
    player_answer = input("請輸入答案：")
    if player_answer == answer:
        print("恭喜你答對了！Boss 受到了 10 點傷害。")
        return True
    else:
        print("答案錯誤！正確答案是：" + answer if reason == "" else "答案錯誤！正確答案是：" + answer + "，因為" + reason)
        print(f"你受到了 {boss_atk} 點傷害。")
        return False

async def random_question(boss_atk):
    questions = [
        ("少了一本書，猜一個成語", "缺一不可", "缺一Book"),
        ("沖天砲為什麼打不到星星？", "星星會閃", "一閃一閃亮晶晶"),
        ("逛joke版的人又叫?", "joker", ""),
        ("「乳交」猜一間醫院名。", "林口長庚", "領口藏根"),
        ("Costco鬧鬼，猜一句成語。", "好事多磨", "好市多魔"),
        ("薏仁被趕出家門，猜一種職業。", "街頭藝人", ""),
        ("什麼樣的人不能去加油站工作(猜成語)", "油腔滑調", "油槍滑掉"),
        ("為何電腦不快樂？因為有__", "D槽", "低潮")
    ]
    question, answer, reason = random.choice(questions)
    return await guess_riddle(question, answer, reason=reason, boss_atk=boss_atk)

async def fight():

    boss = await get_gui("boss2")
    dead = await get_gui("dead")

    here_id, gold, hp, level = await get_all_player_data()
    boss_id, boss_name, boss_hp, boss_atk, boss_def = await get_server_data.get_boss_data(Server.server)

    while True:
        await clear_screen()
        print(boss)
        print()
        print(f"{boss_name} HP: {boss_hp}")
        print()
        print("你的 HP:", hp)
        print()
        won = await random_question(boss_atk)
        if won:
            boss_hp -= 10
            print()
            input("Press Enter to continue...")
        else:
            hp -= boss_atk
            print()
            input("Press Enter to continue...")
        if boss_hp <= 0:
            await clear_screen()
            print(boss)
            print()
            print("你打敗了 Boss！")
            return True
        if hp <= 0:
            await clear_screen()
            print(dead)
            print()
            print("你死了！")
            return False