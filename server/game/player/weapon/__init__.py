from server.game.player import PlayerManager

class Weapon:
    def __init__(self, player: PlayerManager):
        self.player = player

    async def equip(self, weapon_id: int):
        self.player.session.saving.data.player_cur_data.weapon_id = weapon_id
        await self.player.session.saving.save()

    async def unequip(self):
        self.player.session.saving.data.player_cur_data.weapon_id = 0
        await self.player.session.saving.save()