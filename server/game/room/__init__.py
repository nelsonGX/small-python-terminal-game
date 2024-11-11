from ...proto.game import Record
from instance import Room

class RoomManager:
    def __init__(self, saving: Record):
        self.saving = saving
        self.instance = None

    def set_room(self, id: int):
        self.instance = Room(id)

    def get_room(self) -> Room:
        return self.instance
    
    def get_available_rooms(self) -> list:
        return