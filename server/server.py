from pathlib import Path
from server.utils.savings import Savings

async def main():
    directory_path = Path('./saved/')
    for file_path in directory_path.glob('*.bin'):
        data = await Savings.load_file_static(file_path.name.replace('.bin', ''))
        print(data)