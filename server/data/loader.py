from typing import List
import json
import aiofiles

from server.data.data import RoomData

class DataLoader:
    room_data: List[RoomData] = []

    @staticmethod
    async def load_data(file_path: str, data_class):
        async with aiofiles.open(file_path, 'r') as file:
            content = await file.read()
            data_list = json.loads(content)
            return [data_class(**data) for data in data_list]

    @classmethod
    async def initialize(cls):
        DataLoader.room_data = await cls.load_data('./data/RoomData.json', RoomData)