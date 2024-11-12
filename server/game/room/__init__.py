from typing import List

from ...data.data import RoomData
from ...data.loader import DataLoader
from ...proto.game import Record
from .instance import Room

class RoomManager:
    def __init__(self, saving: Record):
        self.saving = saving
        self.instance = None

    # Create a new room instance for specific room ID
    async def set_room(self, room_id: int):
        self.instance = Room(room_id)

    # Get current room instance
    async def get_room(self) -> Room:
        return self.instance

    # Get all available (unfinished) rooms data
    async def get_available_rooms(self) -> List[RoomData]:
        unfinished_list = []
        for room in DataLoader.room_data:
            if not self.is_room_finished(room.ID):
                unfinished_list.append(room)
        return unfinished_list

    # Check if a room is finished
    async def is_room_finished(self, room_id: int):
        room_data = next(
            (room for room in self.saving.player_cur_data.room_info_list if room.id == room_id),
            None
        )
        return room_data.finished if room_data else False