# Call procedure: init -> create_saving / set_saving -> game_start

from pathlib import Path

from .data.loader import DataLoader
from .game.shop import ShopManager
from .game.room import RoomManager
from .game.player import PlayerManager
from .game.buff import BuffManager

from server.utils.saving import Saving

class Server:
    server = None

    def __init__(self):
        # Managers
        self.room: RoomManager | None = None
        self.player: PlayerManager | None = None
        self.shop: ShopManager | None = None
        self.buff: BuffManager | None = None
        # Savings
        self.saving: Saving | None = None
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
    async def set_saving(self, saving: str | Saving):
        self.saving = saving

    # Create manager for current session and saving
    async def game_start(self):
        self.room = RoomManager(self)
        self.player = PlayerManager(self)
        self.shop = ShopManager(self)
        self.buff = BuffManager(self)

    async def game_end(self):
        self.room = None
        self.player = None
        self.shop = None
        await self.saving.save()
        self.saving = None