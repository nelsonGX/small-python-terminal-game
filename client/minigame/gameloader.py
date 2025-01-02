from client.minigame.games.game01 import Game01
from client.minigame.games.game02 import Game02
from client.minigame.games.game03 import Game03
from client.minigame.games.game04 import Game04
from client.minigame.games.game05 import Game05
from client.minigame.games.game06 import Game06
from client.minigame.games.game07 import Game07
from client.minigame.games.game08 import Game08
from client.minigame.games.game09 import Game09
from client.minigame.games.game10 import Game10
from client.minigame.games.game11 import Game11
from server import Server
import os

async def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def play01(game_name):
    await clear_screen()
    game = Game01(Server.server)
    await game.start()

async def play02(game_name):
    await clear_screen()
    game = Game02(Server.server)
    await game.start()

async def play03(game_name):
    await clear_screen()
    game = Game03(Server.server)
    await game.start()

async def play04(game_name):
    await clear_screen()
    game = Game04(Server.server)
    await game.start()

async def play05(game_name):
    await clear_screen()
    game = Game05(Server.server)

async def play06(game_name):
    await clear_screen()
    game = Game06(Server.server)
    await game.start()

async def play07(game_name):
    await clear_screen()
    game = Game07(Server.server)
    await game.start()

async def play08(game_name):
    await clear_screen()
    game = Game08(Server.server)
    await game.start()

async def play09(game_name):
    await clear_screen()
    game = Game09(Server.server)
    await game.start()

async def play10(game_name):
    await clear_screen()
    game = Game10(Server.server)
    await game.start()

async def play11(game_name):
    await clear_screen()
    game = Game11(Server.server)
    await game.start()