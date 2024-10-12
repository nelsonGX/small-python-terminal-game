from pathlib import Path

from server.utils.saving import Saving

class Server:
    server = None

    def __init__(self):
        self.saving = None
        self.savings = []

    async def init(self):
        directory_path = Path('./saved/')
        for file_path in directory_path.glob('*.bin'):
            self.savings.append(Saving(await Saving.load_file_static(file_path.name.replace('.bin', ''))))