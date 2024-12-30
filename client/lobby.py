import asyncio
import os
import sys
import platform

import server
from client.assets.reader import get_gui, get_player, get_gui_properties
from client.renderer import AsyncMapRenderer
import client.minigame.gameloader as gameloader
import client.animations as animations

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

async def render_frame(renderer, player_x, player_y):
    """Asynchronously render a single frame of the game"""
    clear_screen()
    viewport = await renderer.get_viewport(player_x, player_y)
    print(viewport)
    print("\nUse WASD to move, Q to quit")
    print(f"Player position: ({player_x}, {player_y})")

async def main_game_loop():
    game_map = await get_gui("lobby")
    game_properties = await get_gui_properties("lobby")
    game_elements = game_properties["elements"]

    await server.Server.server.game_start()
    
    # Initialize the renderer
    renderer = AsyncMapRenderer(game_map, viewport_width=50, viewport_height=30)
    
    # Player starting position
    player_x = 3
    player_y = 2
    
    while True:
        # Render current frame
        await render_frame(renderer, player_x, player_y)
        
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
        elif key == 'q':
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
                        if element["action"] == "game":
                            await gameloader.play(element["content"])
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