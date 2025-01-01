import asyncio
import os
import sys
import platform

from server import Server
from client.assets.reader import get_gui, get_player, get_gui_properties
from client.renderer import AsyncMapRenderer
import client.minigame.gameloader as gameloader
import client.animations as animations
from client.shop.shop import shop

class get_server_data:
    def __init__(self, session: Server):
        self.session: Server = session

    async def get_gold(self):
        return await self.session.shop.get_owned_currencies()
    async def get_hp(self):
        return await self.session.player.get_hp()
    async def get_hero_id(self):
        return await self.session.player.get_hero_id()
    async def get_level(self):
        return await self.session.player.get_level()
    
async def get_all_data():
    get_data = get_server_data(Server.server)

    hero_id = await get_data.get_hero_id()
    gold = await get_data.get_gold()
    hp = await get_data.get_hp()
    level = await get_data.get_level()

    return hero_id, gold, hp, level
    
# Different input handling for different operating systems
if platform.system() == 'Windows':
    import msvcrt
    
    async def get_key():
        while True:
            if msvcrt.kbhit():
                return msvcrt.getch().decode('utf-8').lower()
            await asyncio.sleep(0.01)
else:
    import termios
    import tty
    
    async def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                if sys.stdin.readable():
                    ch = sys.stdin.read(1)
                    return ch.lower()
                await asyncio.sleep(0.01)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

async def render_frame(renderer, player_x, player_y, hero_id, gold, hp, level):
    """Asynchronously render a single frame of the game"""
    clear_screen()

    print(f"Hero ID: {hero_id} | Gold: {gold} | HP: {hp} | Level: {level}")

    viewport = await renderer.get_viewport(player_x, player_y)
    print(viewport)

    print("\nUse WASD to move, Q to quit")

async def main_game_loop():
    game_map = await get_gui("lobby")
    game_properties = await get_gui_properties("lobby")
    game_elements = game_properties["elements"]

    await Server.server.game_start()

    # Initialize the renderer
    renderer = AsyncMapRenderer(game_map, viewport_width=50, viewport_height=30)
    
    # Player starting position
    player_x = 3
    player_y = 2
    
    while True:
        # get datas
        hero_id, gold, hp, level = await get_all_data()

        # Render current frame
        await render_frame(renderer, player_x, player_y, hero_id, gold, hp, level)
        
        # Get player input asynchronously
        key = await get_key()
        
        # Store current position
        new_x, new_y = player_x, player_y
        
        # Update position based on input
        if key == 'w':
            new_y -= 1
        elif key == 's':
            new_y += 1
        elif key == 'a':
            new_x -= 1
        elif key == 'd':
            new_x += 1

        # quit
        elif key == '\x03' or key == 'q':
            clear_screen()
            title = await get_gui("title")
            print(title)
            print()
            print("Goodbye!")
            break
            
        # Check if new position is within bounds
        if (1 <= new_x < renderer.map_width - 1 and 
            1 <= new_y < renderer.map_height - 1):
            
            try:
                # Get character at the new position directly from map_lines
                new_pos_char = renderer.map_lines[new_y][new_x]
                
                # Check for special elements before moving
                element_found = False
                for element in game_elements:
                    if new_pos_char == element["key"]:
                        await animations.transition()
                        element_found = True
                        if element["action"] == "game01":
                            await gameloader.play01(element["content"])
                        if element["action"] == "game06":
                            await gameloader.play06(element["content"])
                        if element["action"] == "shop":
                            await shop()
                        break
                
                # Only update position if not hitting a border or special element
                if (not element_found and 
                    new_pos_char not in game_properties["border_elements"]):
                    # Update old position
                    await renderer.update_map(player_x, player_y, ' ')
                    
                    # Update player position
                    player_x, player_y = new_x, new_y
                    await renderer.update_map(player_x, player_y, "O")
                else:
                    print(f"Movement blocked by: {new_pos_char}")
            except IndexError as e:
                print(f"Position access error: {e}")
                print(f"Map size: {len(renderer.map_lines)} rows")
                if len(renderer.map_lines) > new_y:
                    print(f"Row length at {new_y}: {len(renderer.map_lines[new_y])}")
            
        # Small delay to prevent too rapid updates
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    # Run the async game loop
    from renderer import AsyncMapRenderer
    from assets.reader import get_gui, get_gui_properties, get_player
    asyncio.run(main_game_loop())