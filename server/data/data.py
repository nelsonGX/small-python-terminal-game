from dataclasses import dataclass

@dataclass
class RoomData:
    ID: int
    LevelLimit: int
    Name: str