import os

from server import Server
from client.animations import loading
from client.assets.reader import get_gui
from client.lobby import main_game_loop

menu_options = [
    {"name": "1. Start New Game", "action": "start_new_game"},
    {"name": "2. Load Game", "action": "load_game"},
    {"name": "3. Exit", "action": "exit"},
    {"name": "4. Test", "action": "test"}
]

async def check_action(index):
    if not index.isdigit():
        return False
    index = int(index)
    return False if index > len(menu_options) else True

async def action(index, title):
    index = int(index)
    index -= 1
    action = menu_options[index]["action"]

    # Make new server object
    Server.server = Server()
    await Server.server.init()

    if action == "start_new_game":
        await loading("Starting new game")
        await Server.server.create_saving("test") # Create new saving
        await main_game_loop()

    elif action == "load_game":
        await loading("Loading game")
        await main_game_loop()

    elif action == "test":
        from client.bossfight.bossloader import fight_boss
        await fight_boss(1)

    elif action == "exit":
        print(title)
        print("Goodbye!")
        exit(0)
    
    return True

async def entry():
    checker = False
    index = 0
    checker_tmp = True
    title = await get_gui("title")
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
    await action(index, title)