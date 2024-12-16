from client.minigame.games.game06 import Game06
from server import Server
import os

async def play(game_name):
    os.system('cls' if os.name == 'nt' else 'clear')
    game = Game06(Server.server)
    await game.start()