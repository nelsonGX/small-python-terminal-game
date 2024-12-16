import aiofiles
import json

async def read_file(file):
    async with aiofiles.open(file, mode='r') as f:
        return await f.read()
    
async def get_gui(gui):
    return await read_file("client/assets/guis/" + gui + ".txt")

async def get_gui_properties(gui):
    return json.loads(await read_file("client/assets/guis/" + gui + ".json"))

async def get_player(player):
    return await read_file("client/assets/player/" + player + ".txt")