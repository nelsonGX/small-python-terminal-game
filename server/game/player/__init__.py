from ...proto.game import Record

class PlayerManager:
    def __init__(self, saving: Record):
        self.saving = saving

    async def get_hp(self) -> int:
        return self.saving.player_cur_data.hp

    async def set_hp(self, hp: int):
        self.saving.player_cur_data.hp = hp