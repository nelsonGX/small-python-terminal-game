import random
import string

from server import Server


class GameGlitch:
    def __init__(self, name, hp, effects, glitch_type, heal_amount=20, random_heal_name=None):
        self.name = name
        self.hp = hp
        self.max_hp = hp  #記錄最大血
        self.effects = effects  #技能及其傷害 {"技能名稱": 傷害}
        self.glitch_type = glitch_type  #錯誤類型，用於屬性克制
        self.heal_amount = heal_amount  #回血技能的回復量
        self.random_heal_name = random_heal_name or self.generate_random_heal_name()

    def apply_effect(self, opponent, effect, type_advantage=None):
        #執行攻擊、屬性
        damage = self.effects[effect]
        damage = random.randint(damage - 5, damage + 5)  #增加浮動

        if type_advantage and opponent.glitch_type in type_advantage.get(effect, []):
            damage = damage * 2
            print(f"屬性克制！{effect} 對 {opponent.name} 造成了加倍傷害！")

        opponent.hp = max(0, opponent.hp - damage)
        print(f"{self.name} 使用了 {effect}！造成了 {damage} 點損害。")
        print(f"{opponent.name} 的遊戲穩定性剩餘 {opponent.hp}。\n")

    def repair(self):
        #回血
        healed = min(self.heal_amount, self.max_hp - self.hp)
        self.hp = self.hp + healed
        print(f"{self.name} 使用了通用修復技能！恢復了 {healed} 點遊戲穩定性。")
        print(f"{self.name} 的遊戲穩定性現在是 {self.hp}。\n")

    def random_heal(self):
        #亂碼，回血
        healed = min(self.heal_amount, self.max_hp - self.hp)
        self.hp = self.hp + healed
        print(f"{self.name} 使用了隨機亂碼技能『{self.random_heal_name}』！恢復了 {healed} 點遊戲不穩定性。")
        print(f"{self.name} 的遊戲不穩定性現在是 {self.hp}。\n")

    def is_resolved(self):
        return self.hp <= 0

    @staticmethod
    def generate_random_heal_name():
        #生成亂碼
        length = random.randint(5, 10)
        return ''.join(random.choices(string.ascii_letters + string.digits + "%!@#$", k=length))


class Player:
    def __init__(self, name, hp, effects, coin=0):
        self.glitch = GameGlitch(name, hp, effects, glitch_type="無")
        self.coin = coin

    def adjust_coin(self, win):
        #調整硬幣
        if win:
            reward = random.randint(20, 45)
            self.coin = self.coin + reward
            print(f"恭喜！你獲得了 {reward} 個硬幣。你現在有 {self.coin} 個硬幣。\n")
        else:
            penalty = random.randint(20, 35)
            self.coin = self.coin - penalty
            if self.coin < 0:
                self.coin = 0  #硬幣不能為負
            print(f"可惜！你損失了 {penalty} 個硬幣。你現在有 {self.coin} 個硬幣。\n")


def npc_choose_action(glitch):
    #NPC隨機行動
    actions = list(glitch.effects.keys()) + ["修復", "亂碼"]
    return random.choice(actions)


def choose_random_glitch(glitches):
    #隨機選擇一個技能
    return random.choice(glitches)


def glitch_battle(player):
    #定義屬性克制
    type_advantage = {
        "吹卡帶": ["高延遲", "遊戲崩潰"],
        "清潔接點": ["圖像錯誤", "音效錯誤"],
        "格式化存檔": ["文字亂碼", "顏色錯誤"],
        "數據修正": ["高延遲", "顏色錯誤"],
        "核心重啟": ["遊戲崩潰", "音效錯誤"]
    }

    #定義多個遊戲錯誤
    glitches = [
        GameGlitch("高延遲", 120, {"延遲尖峰": 20, "封包遺失": 15, "超時": 25}, "高延遲"),
        GameGlitch("圖像錯誤", 100, {"畫面撕裂": 20, "材質延遲": 15, "畫面殘影": 25}, "圖像錯誤"),
        GameGlitch("顏色錯誤", 90, {"顏色互換": 20, "亮度漂移": 15, "顏色條帶": 25}, "顏色錯誤"),
        GameGlitch("文字亂碼", 110, {"文字錯亂": 20, "字符缺失": 15, "字體無法辨識": 25}, "文字亂碼"),
        GameGlitch("遊戲崩潰", 130, {"程序錯誤": 25, "未響應": 20, "死循環": 30}, "遊戲崩潰"),
        GameGlitch("音效錯誤", 100, {"音效死循環": 20, "音檔缺失": 15, "爆音": 25}, "音效錯誤"),
    ]

    while True:
        #隨機選擇遊戲錯誤
        npc_glitch = choose_random_glitch(glitches)
        print(f"一個導致玩家變暴力的 {npc_glitch.name} 出現了！\n")

        #敵方先攻
        print(f"{npc_glitch.name} 將對你發出干擾！\n")
        current_player = "npc"

        #戰鬥迴圈
        while not player.glitch.is_resolved() and not npc_glitch.is_resolved():
            if current_player == "玩家":
                print(f"{player.glitch.name} 的反擊！")
                effects_list = list(player.glitch.effects.keys())
                for i, effect in enumerate(effects_list, 1):
                    print(f"{i}. {effect} (效果值: {player.glitch.effects[effect]} ±5)")
                print(f"{len(effects_list) + 1}. 修復 (恢復 {player.glitch.heal_amount} 點遊戲穩定性)")
                print("輸入 'stop' 結束遊戲。")

                choice = input(f"選擇行動 (1-{len(effects_list) + 1} 或 'stop'): ").strip().lower()

                if choice == "stop":
                    print("遊戲結束。")
                    return

                #驗證輸入是否合法
                try:
                    action_choice = int(choice)
                    if action_choice < 1 or action_choice > len(effects_list) + 1:
                        raise ValueError
                except ValueError:
                    print("錯誤選項，請輸入有效技能或 'stop'！\n")
                    continue

                #執行玩家的行動
                if action_choice == len(effects_list) + 1:
                    player.glitch.repair()
                else:
                    chosen_effect = effects_list[action_choice - 1]
                    player.glitch.apply_effect(npc_glitch, chosen_effect, type_advantage)
            else:
                #NPC隨機選擇行動
                action = npc_choose_action(npc_glitch)
                print(f"{npc_glitch.name} 的回合！")
                if action == "修復":
                    npc_glitch.repair()
                elif action == "亂碼":
                    npc_glitch.random_heal()
                else:
                    npc_glitch.apply_effect(player.glitch, action)

            #判斷是否結束戰鬥
            if player.glitch.is_resolved():
                print(f"{player.glitch.name} 無法維持穩定運行！{npc_glitch.name} 獲勝了！\n")
                player.adjust_coin(win=False)
                break
            elif npc_glitch.is_resolved():
                print(f"{npc_glitch.name} 的問題被解決了！{player.glitch.name} 獲勝了！\n")
                player.adjust_coin(win=True)
                break

            #下一回合
            current_player = "玩家" if current_player == "npc" else "npc"

        #提供是否繼續的選項
        continue_choice = input("是否繼續挑戰下一個遊戲錯誤？(y/n): ").strip().lower()
        if continue_choice != "y":
            print("遊戲結束！")
            break


#初始化玩家
player = Player(name="玩家角色", hp=150, effects={
    "吹卡帶": 30,
    "清潔接點": 25,
    "格式化存檔": 35,
    "數據修正": 28,
    "核心重啟": 40
})

class Game08:
    def __init__(self, session: Server):
        self.session = session

    async def start(self):
        # 開始遊戲
        print("遊戲錯誤出現了！\n")
        glitch_battle(player)
