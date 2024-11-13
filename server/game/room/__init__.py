from typing import List

from ... import Server
from ...data.data import RoomData
from ...data.loader import DataLoader
from .instance import Room

class RoomManager:
    def __init__(self, server: Server):
        self.session = server
        self.instance = None

    # Get all available (unfinished) rooms data
    async def get_available_rooms(self) -> List[RoomData]:
        unfinished_list = []
        # Find unfinished rooms
        for room in DataLoader.room_data:
            if not self.is_room_finished(room.ID):
                unfinished_list.append(room)
        return unfinished_list

    # Check if a room is finished
    async def is_room_finished(self, room_id: int):
        room_data = next(
            (room for room in self.session.saving.data.player_cur_data.room_info_list if room.id == room_id),
            None
        )
        return room_data.finished if room_data else False

    # Create a new room
    @staticmethod
    async def create_room(room_id: int) -> Room:
        return Room(room_id)