import random

from server import Server


def get_split_combinations():
    splits = []
    # 水平相鄰
    for i in range(1, 36):  # 從 1 到 35
        if i % 3 != 0:  # 排除每行的最後一個數字
            splits.append((i, i + 1))
    # 垂直相鄰
    for i in range(1, 34):  # 從 1 到 33
        splits.append((i, i + 3))
    # 與 0 的相鄰數字
    splits.extend([(0, 1), (0, 2), (0, 3)])
    return splits
def get_street_combinations():
    streets=[
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9],
        [10, 11, 12],
        [13, 14, 15],
        [16, 17, 18],
        [19, 20, 21],
        [22, 23, 24],
        [25, 26, 27],
        [28, 29, 30],
        [31, 32, 33],
        [34, 35, 36]
    ]
    return streets
def display_rules():
    print("歡迎來到輪盤遊戲！")
    print("下注規則：")
    print("1. 顏色 (Red/Black/Green)")
    print("2. 奇偶 (Odd/Even)")
    print("3. 大小 (Big/Small)")
    print("4. 12個數字組合(前、中、後)")
    print("5. 直行(第一、第二、第三)")
    print("6. 單個數字 (0-36)")
    print("7. 兩個數字組合")
    print("8. 三個數字組合")
def spin_roulette():
    number = random.randint(0, 36)  # 轮盘上的数字范围
    oddNeven = "Even" if number % 2 == 0 else "Odd"  
    color = "Red" if number in [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36] else "Black" 
    return number, color, oddNeven
def get_user_bet():
    while True:  # 用來檢查 bet_type 是否有效
        bet_type = input("請選擇下注的類型：").lower()
        if bet_type in [ "顏色", "奇偶", "大小", "12個數字組合", "直行", "單個數字", "兩個數字組合", "三個數字組合"]:
            break  # bet_type 有效，跳出迴圈
        else:
            print("無效的下注類型，請重新輸入！")
    # 根據有效的 bet_type 繼續下注邏輯
    if bet_type == "顏色":
        while True:
            bet = input("請輸入下注的顏色 (Red/Black)：").capitalize()  # capitalize() 第一個字母大寫
            if bet in ["Red", "Black"]:
                break  # 跳出迴圈
            else:
                print("無效的下注值，請輸入 Red 或 Black！")
    elif bet_type == "奇偶":
        while True:
            bet = input("請輸入下注的奇或偶 (Odd/Even)：").capitalize()
            if bet in ["Odd", "Even"]:
                break  # 跳出迴圈
            else:
                print("無效的下注值，請輸入 Odd 或 Even！")
    elif bet_type == "大小":
        while True:
            bet = input("請輸入下注的大小 (Big/Small)：").capitalize()
            if bet in ["Big", "Small"]:
                break  # 跳出迴圈
            else:
                print("無效的下注值，請輸入 Big 或 Small！")
    elif bet_type == "12個數字組合":
        while True:
            bet = input("請輸入下注的數字組合 (前、中、後)：")
            if bet in ["前", "中", "後"]:
                break  # 跳出迴圈
            else:
                print("無效的下注值，請輸入 前、中、後！")
    elif bet_type == "直行":
        while True:
            bet = input("請輸入下注的直行 (第一、第二、第三)：").capitalize()
            if bet in ["第一", "第二", "第三"]:
                break  # 跳出迴圈
            else:
                print("無效的下注值，請輸入 第一、第二、第三！")
    elif bet_type == "單個數字":
        while True:
            try:
                bet = int(input("請輸入下注的數字 (0-36)："))
                if 0 <= bet <= 36:  # 確保數字在範圍內
                    break  # 跳出迴圈
                else:
                    print("無效的下注值，請輸入 0 到 36 之間的數字！")
            except ValueError:
                print("無效的輸入，請輸入有效的數字！")
    elif bet_type == "兩個數字組合":
        while True:
            valid_splits = get_split_combinations()
            try:
                bet = input("請輸入下注的範圍ex.(0-2、3-6...)：")
                bet = bet.split("-")  # 將數字範圍分成兩個數字
                bet1, bet2 = int(bet[0]), int(bet[1])
                if (bet1, bet2) in valid_splits or (bet2, bet1) in valid_splits:  # 確保範圍在允許的範圍內
                    break  # 跳出迴圈
                else:
                    print("無效的下注值，請輸入允許的範圍！")
            except ValueError:
                print("無效的輸入，請輸入有效的數字！")
    elif bet_type == "三個數字組合":
        while True:
            try:
                bet = int(input("請選擇下注的行號（1-12）："))
                if 1<= bet <= 12:  # 確保行號在範圍內
                    streets=get_street_combinations()
                    bet = streets[bet-1]  # 將行號轉換為數字組合
                    break  # 跳出迴圈
                else:
                    print("無效的下注值，請輸入 1 到 12 之間的行號！")
            except ValueError:
                print("無效的輸入，請輸入有效的數字！")
    return bet_type, bet
def check_result(bet_type, bet, result_number, result_color,result_oddNeven):
    print(f"輪盤結果：數字{result_number},顏色{result_color},奇偶{result_oddNeven}")
    if bet_type == "顏色":
        return bet == result_color
    elif bet_type == "奇偶":
        if result_number == 0:  # 特殊情况：0 既不是奇数也不是偶数
            return False
        return bet == result_oddNeven
    elif bet_type == "大小":
        if result_number > 12:
            resultSize = "Big"
            if resultSize == bet:
                return True
        elif result_number > 0:
            resultSize = "Small"
            if resultSize == bet:
                return True
        else:
            return False
    elif bet_type == "12個數字組合":
        if 12 >= result_number > 0:
            position = "前"
            if position == bet:
                return True
        elif 24 >= result_number > 12:
            position = "中"
            if position == bet:
                return True
        elif 36 >= result_number > 24:
            position = "後"
            if position == bet:
                return True
        elif result_number == 0:
            return False   
    elif bet_type == "直行":
        if result_number in [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34] and bet == "第一":
            return True
        elif result_number in [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35] and bet == "第二":
            return True
        elif result_number in [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36] and bet == "第三":
            return True
    elif bet_type == "單個數字":
        return bet == result_number
    elif bet_type == "兩個數字組合":
        return result_number in bet
    elif bet_type == "三個數字組合":
        return result_number in bet

class Game04:
    def __init__(self, session: Server):
        self.session = session

    async def start(self):
        display_rules()
        while True:
            bet_type, bet = get_user_bet()  # 解構復職
            result_number, result_color, result_oddNeven = spin_roulette()
            if check_result(bet_type, bet, result_number, result_color, result_oddNeven):
                print("恭喜！你赢了！")
            else:
                print("很遺憾，你輸了。")

            play_again = input("是否再玩一局？(y/n): ").lower()
            if play_again != 'y':
                print("感謝遊玩，再見！")
                break
