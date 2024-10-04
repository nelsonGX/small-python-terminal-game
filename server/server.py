from pathlib import Path
from server.utils import encryption

async def main():
    directory_path = Path('./saved/')
    for file_path in directory_path.glob('*.bin'):
        data = await encryption.load(file_path.name.replace('.bin', ''))
        print(data)