from server.game.player.weapon import Weapon
from ... import Server
from ...data.loader import DataLoader
from ...proto.game import Retcode


class PlayerManager:
    def __init__(self, server: Server):
        self.session = server
        self.weapon = Weapon(self)
        self.ATK = 0
        self.DEF = 0

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

    # Get player hero type
    async def get_hero_id(self):
        return self.session.saving.data.player_cur_data.hero_id

    # Calculate ATK and DEF
    async def calc_stats(self) -> Retcode:
        # Get curve data
        curve_data = next(
            (info for info in DataLoader.upgrade_curve_data if info.ID == self.get_hero_id()),
            None
        )
        # Check if curve data exists
        if curve_data is None:
            return Retcode.HERO_NOT_FOUND
        # Get hero data
        hero_data = next(
            (info for info in DataLoader.hero_data if info.ID == self.get_hero_id()),
            None
        )
        # Check if hero data exists
        if hero_data is None:
            return Retcode.HERO_NOT_FOUND
        # Calculate stats
        self.ATK = hero_data.BaseAtk * (await self.get_level() ** curve_data.Atk)
        self.DEF = hero_data.BaseDef * (await self.get_level() ** curve_data.Def)
        # Return success
        return Retcode.SUCCESS