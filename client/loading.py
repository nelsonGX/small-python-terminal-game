import random
import asyncio
import os
from client.assets.reader import get_gui

loading_bar = """------------------------
|%%%%%%%%%%%%%%%%%%%%%%|
------------------------
"""

loading_content = "▇"


async def loading(title):
    logo = await get_gui("title")
    os.system("clear")
    max_size = loading_bar.count("%")
    for i in range(max_size + 1):
        print(logo)
        print(title)
        print(loading_bar.replace("%", loading_content * i, 1).replace("%", " " * (max_size - i), 1).replace("%", ""), end="")
        await asyncio.sleep(random.uniform(0.01, 0.05))
        os.system("clear")
    print("Loaded!")

# testing
if __name__ == "__main__":
    asyncio.run(loading())