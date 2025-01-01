import random

from client.assets.reader import get_gui

async def guess_riddle(question, answer, reason=""):
    print("\n猜謎遊戲！")
    print(question)
    player_answer = input("請輸入答案：")
    if player_answer == answer:
        print("恭喜你答對了！Boss 受到了 10 點傷害。")
        return True
    else:
        print("答案錯誤！正確答案是：" + answer if reason == "" else "答案錯誤！正確答案是：" + answer + "，因為" + reason)
        return False

async def random_question():
    questions = [
        ("少了一本書，猜一個成語", "缺一不可", "缺一Book"),
        ("沖天砲為什麼打不到星星？", "星星會閃", "一閃一閃亮晶晶"),
        ("逛joke版的人又叫?", "Joker"),
        ("「乳交」猜一間醫院名。", "林口長庚", "領口藏根"),
        ("Costco鬧鬼，猜一句成語。", "好事多磨", "好市多魔"),
        ("薏仁被趕出家門，猜一種職業。", "街頭藝人"),
        ("什麼樣的人不能去加油站工作(猜成語)", "油腔滑調", "油槍滑掉"),
        ("為何電腦不快樂？因為有__", "D槽", "低潮")
    ]
    question, answer, reason = random.choice(questions)
    return await guess_riddle(question, answer, reason)

async def fight():
    while True:
        won = await random_question()