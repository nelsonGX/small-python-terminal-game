from typing import List

from server import Server
from server.data.data import MinigameData
from server.data.loader import DataLoader
from server.game.minigame.instance import Minigame


class MinigameManager:
    def __init__(self, server: Server):
        self.session = server

    # Get all available (unfinished) rooms data
    async def get_available_minigames(self) -> List[MinigameData]:
        unfinished_list = []
        # Find unfinished rooms
        for room in DataLoader.minigame_data:
            if not self.is_room_finished(room.ID):
                unfinished_list.append(room)
        return unfinished_list

    # Get minigames for current level
    async def get_level_minigames(self) -> List[MinigameData]:
        unfinished_list = []
        for room in DataLoader.minigame_data:
            if room.LevelLimit == self.session.player.get_level():
                unfinished_list.append(room)
        return unfinished_list

    # Check if a room is finished
    async def is_room_finished(self, minigame_id: int):
        minigame_data = next(
            (info for info in self.session.saving.data.player_cur_data.minigame_info_list if info.id == minigame_id),
            None
        )
        return minigame_data.finished if minigame_data else False

    # Create a new minigame instance
    async def create_game_instance(self, minigame_id: int) -> Minigame:
        return Minigame(minigame_id, self)