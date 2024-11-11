import json
from typing import List

from server.data.data import RoomData

class DataLoader:
    room_data: List[RoomData] = []

    @staticmethod
    def load_data(file_path: str, data_class):
        with open(file_path, 'r') as file:
            data_list = json.load(file)
            return [data_class(**data) for data in data_list]

    @classmethod
    def initialize(cls):
        DataLoader.room_data = cls.load_data('./data/RoomData.json', RoomData)