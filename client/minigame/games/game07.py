'''
Jenna's Game:
玩家選擇場上的一隻魔獸（等級1～5）
莊家派出隨機一隻魔獸（等級為玩家等級-2～玩家等級+2之間，但介於1～5之間）

玩家有0.6的機率使出一般攻擊（攻擊力=等級）、0.3的機率使出雙重攻擊（攻擊力=等級*2）、0.1的機率使出神秘大招（攻擊力=等級*（亂數3～5））
莊家有0.4的機率使出一般攻擊（攻擊力=等級）、0.4的機率使出雙重攻擊（攻擊力=等級*2）、0.2的機率使出神秘大招（攻擊力=等級*（亂數3～5））

每次對戰開始前，玩家需下注（賭注以金幣計），賠率根據玩家與莊家魔獸的等級比例計算：
賠率 = (玩家等級 / 莊家等級) + 隨機亂數(0.5～1.5)

玩家先進行攻擊，攻擊效果如下：
- 若莊家成功開啟防護罩（20%機率），攻擊無效
- 若未防禦成功，則血量減少相應攻擊傷害

莊家攻擊規則與玩家相同，玩家亦有20%的機率開啟防護罩。

雙方皆有10點血量，先扣完血量的一方輸掉：
- 若玩家贏得比賽，獲得賭注×賠率的金幣，並加入抽獎環節。
- 若莊家贏得比賽，玩家失去賭注金幣。

抽獎(LuckyDraw)環節：若玩家選擇參加（Y/N），隨機亂數決定獎品：
    亂數<0.1:獲得等級5的魔寵
    亂數>=0.1 and <0.3:獲得等級3的魔寵
    亂數>=0.3 and <0.5:獲得等級3的寶物
    亂數>=0.5 and <0.7:獲得賭注×3的金幣
    其餘情況：獲得賭注金幣

若玩家勝利，需寫出「玩家勝利！莊家給予玩家賭注×賠率金幣」。
若莊家勝利，需寫出「莊家勝利！玩家請再接再厲」。

設定：
莊家血條：PHP=10
玩家血條：SHP=10

莊家等級：PLevel=隨機1～5
玩家等級：SLevel=玩家輸入1～5

賭注金幣：bet（玩家下注）
玩家初始金幣：SGold=500
賠率：odds = (SLevel / PLevel) + 隨機(0.5～1.5)
'''
from server import Server

'''
攻擊名稱要依所選取的魔獸做變換
'''
import random as rd

class Game07:
    def __init__(self, session: Server):
        self.session = session

    async def start(self):
        # 初始設定
        PHP = 10  # 莊家血量
        SHP = 10  # 玩家血量
        SGold = 500  # 玩家初始金幣

        print("歡迎來到賭場鬥獸場！挑選你的魔獸與莊家對戰，豪賭一場吧！")

        # 玩家選擇等級
        SLevel = int(input("請選擇你的魔獸等級 (1到5): "))
        PLevel = rd.randint(max(1, SLevel - 2), min(5, SLevel + 2))
        print(f"莊家派出了等級 {PLevel} 的魔獸！")

        # 玩家設置賭注
        while True:
            bet = int(input(f"請輸入賭注金幣數量 (你總共有 {SGold} 枚金幣): "))
            if 0 < bet <= SGold:
                break
            else:
                print("賭注必須在你擁有的金幣範圍內。")

        # 設定賠率
        odds = round((SLevel / PLevel) + rd.uniform(0.5, 1.5), 2)
        print(f"賭局賠率為：{odds} 倍！")

        Round = 1  # 回合計數

        while PHP > 0 and SHP > 0:
            print(f"\n= Round {Round} ===============")
            print(f"玩家 HP: {SHP} v.s 莊家 HP: {PHP}")

            # 玩家攻擊
            Attack = rd.random()
            if Attack < 0.6:
                PAtt = SLevel
                print("玩家使出了一般攻擊！")
            elif Attack < 0.9:
                PAtt = SLevel * 2
                print("玩家使出了雙重攻擊！")
            else:
                PAtt = SLevel * rd.randint(3, 5)
                print("玩家使出了神秘大招！")

            # 莊家防護罩機會
            if rd.random() < 0.2:
                PAtt = 0
                print("莊家開啟了防護罩，玩家的攻擊無效！")
            else:
                PHP -= PAtt
                print(f"玩家對莊家造成了 {PAtt} 的傷害！")

            if PHP <= 0:
                SGold += int(bet * odds)
                print(f"玩家勝利！莊家給予玩家 {int(bet * odds)} 金幣！")
                print(f"玩家目前金幣數量：{SGold}")

                # LuckyDraw 環節
                LuckyDraw = input("你想參加抽獎嗎？(Y/N): ").upper()
                if LuckyDraw == "Y":
                    print("\n= 抽獎環節 ===============")
                    LDResult = rd.random()
                    if LDResult < 0.1:
                        print("恭喜！你獲得了一隻等級 5 的魔寵！")
                    elif LDResult < 0.3:
                        print("恭喜！你獲得了一隻等級 3 的魔寵！")
                    elif LDResult < 0.5:
                        print("恭喜！你獲得了一件等級 3 的寶物！")
                    elif LDResult < 0.7:
                        BonusGold = bet * 3
                        SGold += BonusGold
                        print(f"恭喜！你獲得了 {BonusGold} 金幣！")
                    else:
                        print("OhNo! 你沒有獲得額外的獎品")

                    print(f"玩家目前金幣數量：{SGold}")

                break

            # 莊家攻擊
            Attack = rd.random()
            if Attack < 0.4:
                SAtt = PLevel
                print("莊家使出了一般攻擊！")
            elif Attack < 0.8:
                SAtt = PLevel * 2
                print("莊家使出了雙重攻擊！")
            else:
                SAtt = PLevel * rd.randint(3, 5)
                print("莊家使出了神秘大招！")

            # 玩家防護罩機會
            if rd.random() < 0.2:
                SAtt = 0
                print("玩家開啟了防護罩，莊家的攻擊無效！")
            else:
                SHP -= SAtt
                print(f"莊家對玩家造成了 {SAtt} 的傷害！")

            if SHP <= 0:
                SGold -= bet
                print(f"莊家勝利！玩家請再接再厲。")
                print(f"玩家失去了 {bet} 金幣！")
                print(f"玩家目前金幣數量：{SGold}")
                break

            Round += 1