async def guess_riddle(question, answer):
    print("\n猜謎遊戲！")
    print(question)
    player_answer = input("請輸入答案：")
    if player_answer == answer:
        print("恭喜你答對了！獲得 50 金幣。")
    else:
        print("答案錯誤！")

async def fight():
    pass