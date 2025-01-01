import random

from server import Server


def _generate_target():
    """Generate a 4-digit number with unique digits."""
    return ''.join(random.sample('0123456789', 4))


class Game10:
    def __init__(self, session: Server):
        self.session = session
        self.target_number = _generate_target()

    def _evaluate_guess(self, guess):
        """Evaluate the guess and return the result as 'xAyB'."""
        a = sum(1 for x, y in zip(self.target_number, guess) if x == y)
        b = sum(1 for char in guess if char in self.target_number) - a
        return f"{a}A{b}B"

    async def start(self):
        print("歡迎來到1A2B遊戲")
        print("請輸入四位數的數字已猜出數值")

        attempts = 0
        while True:
            guess = input("請輸入數字：")
            if not guess.isdigit() or len(guess) != 4 or len(set(guess)) != 4:
                print("輸入值錯誤！請輸入四位數的數字")
                continue

            attempts += 1
            result = self._evaluate_guess(guess)

            if result == "4A0B":
                print(f"恭喜你猜中了答案：{self.target_number}，總共嘗試了{attempts}次！")
                break

            print(result)