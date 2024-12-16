import random
import asyncio
import os

loading_bar = """
------------------------
|%%%%%%%%%%%%%%%%%%%%%%|
------------------------
"""

loading_content = "▇"


async def loading(title):
    os.system("clear")
    max_size = loading_bar.count("%")
    for i in range(max_size + 1):
        print(title)
        print(loading_bar.replace("%", loading_content * i, 1).replace("%", " " * (max_size - i), 1).replace("%", ""))
        await asyncio.sleep(random.uniform(0.01, 0.05))
        os.system("clear")
    print("Loaded!")

# testing
if __name__ == "__main__":
    asyncio.run(loading())