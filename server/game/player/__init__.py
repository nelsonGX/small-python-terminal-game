from server.game.player.weapon import Weapon
from ... import Server

class PlayerManager:
    def __init__(self, server: Server):
        self.session = server
        self.weapon = Weapon(self)

    # Get current player level
    async def get_level(self):
        return self.session.saving.data.player_cur_data.level

    # Set current player level
    async def set_level(self, level: int):
        self.session.saving.data.player_cur_data.level = level
        await self.session.saving.save()

    # Get current player HP
    async def get_hp(self) -> int:
        return self.session.saving.data.player_cur_data.hp

    # Set current player HP
    async def set_hp(self, hp: int):
        self.session.saving.data.player_cur_data.hp = hp
        await self.session.saving.save()