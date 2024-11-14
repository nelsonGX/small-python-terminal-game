from server.data.data import BossData


class Boss:
    def __init__(self, excel: BossData):
        self.excel: BossData = excel
        self.HP = excel.HP

    async def set_hp(self, hp: int):
        self.HP = hp

    async def get_hp(self) -> int:
        return self.HP