import string
from datetime import datetime
from random import random

import aiofiles

from .encryption import decrypt, encrypt
from ..proto import game
from ..proto.game import HeroType

class Saving:
    def __init__(self, data: game.Record | str):
        if type(data) == str:
            self.data = game.Record(
                player_info=game.PlayerBasicInfo(
                    name=data,
                    pid=''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
                    create_time=int(datetime.now().timestamp()),
                    type=HeroType.NONE,
                ),
                player_cur_data=game.PlayerCurrentData(
                    hero_id=0,
                    level=1,
                    hp=1000,
                    exp=0,
                    weapon_id=0,
                    room_info_list=[],
                ),
                last_save_timestamp=int(datetime.now().timestamp()),
            )
        else:
            self.data = data

    async def set(self, data: game.Record):
        self.data = data

    async def get(self):
        return self.data

    async def save(self):
        async with aiofiles.open("./saved/{}.yanx".format(self.data.player_info.pid), "wb") as binary_file:
            self.data.last_save_timestamp = int(datetime.now().timestamp())
            await encrypt(binary_file, self.data)

    async def load_from_file(self, name: str):
        async with aiofiles.open("./saved/{}.yanx".format(name), "rb") as binary_file:
            self.data = game.Record().parse(await decrypt(binary_file))

    @staticmethod
    async def load_file_static(name: str) -> game.Record:
        async with aiofiles.open("./saved/{}.yanx".format(name), "rb") as binary_file:
            return game.Record().parse(await decrypt(binary_file))