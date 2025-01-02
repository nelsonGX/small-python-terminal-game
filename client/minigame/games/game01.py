import random as rd

from server import Server


async def pause():
    """暫停等待用戶輸入繼續"""
    input("按下 Enter 繼續...")


class Game01:
    """賭場系統類別"""

    def __init__(self, session: Server):
        self.session: Server = session

    async def start(self):
        """進入賭場的主選單"""
        # Get player currency
        currency: int = await self.session.shop.get_owned_currencies()
        print(f"歡迎來到賭場！你有 {currency} 金幣。")
        while True:
            print("\n選擇遊戲：")
            print("1. 骰子遊戲 (無入場費)")
            print("2. 21點 (入場費: 50 金幣)")
            print("3. 拉霸機 (入場費: 100 金幣)")
            print("4. 離開賭場")
            choice = input("請選擇遊戲 (1/2/3/4)：")

            if choice == "1":
                await self.play_dice_game()
            elif choice == "2":
                if await self.check_coins(50):
                    await self.play_blackjack()
            elif choice == "3":
                if await self.check_coins(100):
                    await self.play_slot_machine()
            elif choice == "4":
                print("你離開了賭場。")
                await pause()
                break
            else:
                print("無效的選擇，請重新選擇！")

    async def check_coins(self, cost):
        """檢查金幣是否足夠"""
        currency: int = await self.session.shop.get_owned_currencies()
        if currency >= cost:
            new = currency - cost
            await self.session.shop.set_owned_currencies(new)
            return True
        else:
            print(f"金幣不足！需要 {cost} 金幣，但你只有 {currency} 金幣。")
            return False

    async def play_dice_game(self):
        """骰子遊戲：比大小"""
        print("\n進行骰子遊戲！")
        player_dice = rd.randint(1, 6) + rd.randint(1, 6)
        computer_dice = rd.randint(1, 6) + rd.randint(1, 6)
        print(f"你擲出了 {player_dice} 點，電腦擲出了 {computer_dice} 點。")

        if player_dice > computer_dice:
            print("你贏了！獲得 20 金幣。")
            currency: int = await self.session.shop.get_owned_currencies()
            new = currency + 20
            await self.session.shop.set_owned_currencies(new)
        else:
            print("你輸了！")
        await pause()

    async def play_blackjack(self):
        """21點遊戲"""
        print("\n進行 21 點遊戲！")

        async def draw_card():
            return rd.randint(1, 11)

        player_hand = [await draw_card(), await draw_card()]
        dealer_hand = [await draw_card(), await draw_card()]

        async def hand_value(hand):
            return sum(hand)

        while await hand_value(player_hand) < 21:
            print(f"你的手牌: {player_hand} (總點數: {await hand_value(player_hand)})")
            action = input("選擇行動：1. 要牌 2. 停牌 ")
            if action == "1":
                player_hand.append(await draw_card())
            elif action == "2":
                break
            else:
                print("無效的選擇，請重新選擇。")

        while await hand_value(dealer_hand) < 17:
            dealer_hand.append(await draw_card())

        print(f"你的手牌: {player_hand} (總點數: {await hand_value(player_hand)})")
        print(f"莊家的手牌: {dealer_hand} (總點數: {await hand_value(dealer_hand)})")

        if await hand_value(player_hand) > 21:
            print("你爆了！輸掉了比賽。")
        elif await hand_value(dealer_hand) > 21 or await hand_value(player_hand) > await hand_value(dealer_hand):
            print("你贏了！獲得 250 金幣。")
            currency: int = await self.session.shop.get_owned_currencies()
            new = currency + 250
            await self.session.shop.set_owned_currencies(new)
        else:
            print("你輸了！")
        await pause()

    async def play_slot_machine(self):
        """拉霸機遊戲"""
        print("\n進行拉霸機遊戲！")
        symbols = ["🍒", "🍋", "🔔", "⭐", "7️⃣"]

        def spin_reels():
            return [rd.choice(symbols) for _ in range(3)]

        reels = spin_reels()
        print(f"拉霸機結果: {' '.join(reels)}")

        if reels[0] == reels[1] == reels[2]:
            if reels[0] == "7️⃣":
                print("恭喜！你中了 1000 金幣！")
                currency: int = await self.session.shop.get_owned_currencies()
                new = currency + 1000
                await self.session.shop.set_owned_currencies(new)
            else:
                print("恭喜！你中了 500 金幣！")
                currency: int = await self.session.shop.get_owned_currencies()
                new = currency + 500
                await self.session.shop.set_owned_currencies(new)
        elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
            print("恭喜！你中了 100 金幣！")
            currency: int = await self.session.shop.get_owned_currencies()
            new = currency + 10
            await self.session.shop.set_owned_currencies(new)
        else:
            print("很遺憾，未中獎！")
        await pause()