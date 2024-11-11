from pathlib import Path
from proto.game import Record
from game.room import RoomManager
from game.player import PlayerManager

from server.utils.saving import Saving

class Server:
    server = None

    def __init__(self):
        self.room: RoomManager = None
        self.player: PlayerManager = None
        self.saving: Record = None
        self.savings = []

    async def init(self):
        directory_path = Path('./saved/')
        for file_path in directory_path.glob('*.yanx'):
            self.savings.append(Saving(await Saving.load_file_static(file_path.name.replace('.yanx', ''))))

    async def create_saving(self, name: str):
        saving = Saving(name)
        saving.save()
        self.saving = saving
        self.init()

    async def set_saving(self, saving: str | Record):
        if type(saving) == str:
            self.saving = Saving(await Saving.load_file_static(saving + ".yanx"))
        else:
            self.saving = saving

    async def game_start(self):
        self.room = RoomManager(self.saving)
        self.player = PlayerManager(self.saving)