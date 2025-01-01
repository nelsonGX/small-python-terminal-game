from server import Server
from .game01 import pause


class Game09:
    def __init__(self, session: Server):
        print()

    async def start(self):
        # Original list of letters
        letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]

        # Reverse the list
        reversed_letters = letters[::-1]

        char_list = ["h", "o", "l", "y", "s", "h", "i", "t"]

        print("請將下列哥布林文翻譯成英文字母：", end="")
        for char in char_list:
            print(reversed_letters[letters.index(char)], end="")

        while True:
            input_str = str(input("\n> "))
            if input_str != "".join(char_list):
                print("答錯了，請再次嘗試。")
                continue
            else:
                break

        print("恭喜你答對了！")
        pause()