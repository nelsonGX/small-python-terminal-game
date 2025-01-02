import os

from server import Server
from client.assets.reader import get_gui

class get_server_data:
    def __init__(self, session: Server):
        self.session: Server = session

    async def get_player_gold(self):
        return await self.session.shop.get_owned_currencies()
    
    async def set_gold(self, gold):
        await self.session.shop.set_owned_currencies(gold)

    async def get_server_shop_data(self):
        return await self.session.shop.get_available_items()

async def get_gold():
    get_data = get_server_data(Server.server)
    return await get_data.get_player_gold()

async def set_gold(gold):
    set_data = get_server_data(Server.server)
    await set_data.set_gold(gold=gold)

async def get_shop_data():
    get_data = get_server_data(Server.server)
    return await get_data.get_server_shop_data()

async def get_menu_options():
    data = await get_shop_data()

    # Transform the data
    menu_options = [
        {
            "name": f"{i+1}. {item.ItemName} {item.ItemCost}$",
            "action": "buy",
            "price": item.ItemCost
        }
        for i, item in enumerate(data)
    ]

    # Add the exit option at the end
    menu_options.append({
        "name": f"{len(data)+1}. 離開商店",
        "action": "exit"
    })

    return menu_options

async def check_action(index):
    menu_options = await get_menu_options()
    if not index.isdigit():
        return False
    index = int(index)
    return False if index > len(menu_options) else True

async def action(index, title):
    menu_options = await get_menu_options()
    index = int(index)
    index -= 1
    action = menu_options[index]["action"]

    if action == "buy":
        price = menu_options[index]["price"]
        gold = await get_gold()
        if gold >= price:
            await set_gold(gold - price)
            print("You bought an item!")
            print(f"Gold: {gold} -> {gold - price}")
            print()
            input("Press Enter to continue...")
        else:
            print("Not enough gold!")
            print()
            input("Press Enter to continue...")

    elif action == "exit":
        print(title)
        print("Goodbye!")
        return True
    
    return False

async def shop():
    menu_options = await get_menu_options()
    while True:
        checker = False
        index = 0
        checker_tmp = True
        title = await get_gui("shop")
        os.system("clear")
        while not checker:
            print(title)
            print("Menu:")
            for option in menu_options:
                print(option["name"])
            if not checker_tmp:
                print("\nInvalid option !")
            index = input("Enter option: ")
            checker_tmp = await check_action(index)
            checker = checker_tmp
            os.system("clear")
        exit = await action(index, title)
        if exit:
            break