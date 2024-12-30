from client.minigame.games.game01 import Game01
from client.minigame.games.game06 import Game06
from server import Server
import os

async def play01(game_name):
    os.system('cls' if os.name == 'nt' else 'clear')
    game = Game06(Server.server)
    await game.start()

async def play06(game_name):
    os.system('cls' if os.name == 'nt' else 'clear')
    game = Game01(Server.server)
    await game.start()