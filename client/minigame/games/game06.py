from click import pause

from server.data.loader import DataLoader, BuffData
from server import Server
import random


async def random_buff() -> BuffData:
    prob_list = []
    for buff in DataLoader.buff_data:
        prob_list.append(buff.Probability)
    return random.choices(DataLoader.buff_data, weights=prob_list, k=1)[0]


class Game06:
    def __init__(self, session: Server):
        self.session: Server = session

    async def start(self):
        while True:
            print("請選擇選項")
            print("1. 抽取效果")
            print("2. 離開")
            
            user_input = input("> ")
            try:
                user_input = int(user_input)
                if user_input == 1:
                    # Get player currency
                    currency: int = await self.session.shop.get_owned_currencies()
                    # Check for currencies
                    if currency < 100:
                        print("目前金幣不足，請在獲取 100 金幣後再次嘗試")
                        pause()
                        return
                    # Do calculations
                    await self.session.shop.set_owned_currencies(currency - 100)
                    buff: BuffData = await random_buff()
                    print(f"獲取到的效果為：{buff.Name}！")
                    await self.session.buff.add_buff(buff.ID)
                    pause()
                elif user_input == 2:
                    break
                else:
                    print("無效選項，請選擇 1 或 2。")
                    pause()
            except ValueError:
                print("輸入值錯誤！請輸入數字。")
    