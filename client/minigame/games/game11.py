import random

from client.minigame.games.game01 import pause
from server import Server


class Game11:
    def __init__(self):
        # self.session = session
        print()

    def start(self):
        random_int = random.randint(1, 100)
        print("歡迎來到終極密碼小遊戲！")
        print("請猜數字於1至100之間")
        while True:
            input_int = int(input("> "))
            if input_int == random_int:
                print("恭喜你猜對了！")
                pause()
                break
            else:
                if input_int < random_int:
                    print(f"該數字大於{input_int}！")
                else:
                    print(f"該數字小於{input_int}！")