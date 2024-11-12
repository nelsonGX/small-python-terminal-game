from ...proto.game import Record

class PlayerManager:
    def __init__(self, saving: Record):
        self.saving = saving

    # Get current player HP
    async def get_hp(self) -> int:
        return self.saving.player_cur_data.hp

    # Set current player HP
    async def set_hp(self, hp: int):
        self.saving.player_cur_data.hp = hp