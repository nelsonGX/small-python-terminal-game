from server.data.loader import DataLoader
from server.game.room import RoomManager
from server.game.room.boss import Boss


class Room:
    def __init__(self, room_id: int, manager: RoomManager):
        self.manager = manager
        self.excel = next(
            (info for info in DataLoader.room_data if info.ID == room_id),
            None
        )
        self.boss = Boss(next(
            (info for info in DataLoader.boss_data if info.ID == self.excel.BossID),
            None
        ))