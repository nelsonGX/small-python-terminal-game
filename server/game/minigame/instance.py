from server.game.minigame import MinigameManager


class Minigame:
    def __init__(self, minigame_id: int, manager: MinigameManager):
        self.id = minigame_id
        self.manager = manager