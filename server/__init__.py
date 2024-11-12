# Call procedure: init -> create_saving / set_saving -> game_start

from pathlib import Path

from .data.loader import DataLoader
from .proto.game import Record
from .game.room import RoomManager
from .game.player import PlayerManager

from server.utils.saving import Saving

class Server:
    server = None

    def __init__(self):
        self.room: RoomManager | None = None
        self.player: PlayerManager | None = None
        self.saving: Record | None = None
        self.savings = []

    # Initialize server basic data
    async def init(self):
        # Init savings
        directory_path = Path('./saved/')
        for file_path in directory_path.glob('*.yanx'):
            self.savings.append(Saving(await Saving.load_file_static(file_path.name.replace('.yanx', ''))))
        # Init data
        await DataLoader.initialize()

    # Create a new saving, and assign to current session
    async def create_saving(self, name: str):
        saving = Saving(name)
        await saving.save()
        self.saving = saving
        await self.init()

    # Set the saving for current session to the specified saved data
    async def set_saving(self, saving: str | Record):
        if type(saving) == str:
            self.saving = Saving(await Saving.load_file_static(saving + ".yanx"))
        else:
            self.saving = saving

    # Create manager for current session and saving
    async def game_start(self):
        self.room = RoomManager(self.saving)
        self.player = PlayerManager(self.saving)