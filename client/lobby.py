import asyncio
import os
import sys
import platform
from client.assets.reader import get_gui, get_player, get_gui_properties
from client.renderer import AsyncMapRenderer

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
    # Initialize the renderer
    renderer = AsyncMapRenderer(game_map, viewport_width=50, viewport_height=30)
    
    # Player starting position (where @ is)
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
            
        # Check if new position is at least one space away from map boundaries
        if (1 <= new_x < renderer.map_width - 1 and 
            1 <= new_y < renderer.map_height - 1):
            
            # Get the viewport for the new position
            viewport = await renderer.get_viewport(new_x, new_y)
            current_lines = viewport.split('\n')
            center_y = len(current_lines) // 2
            center_x = len(current_lines[0]) // 2
            
            # Update player position if the space is empty
            if current_lines[center_y][center_x] not in game_properties["border_elements"]:
                # Update old position
                await renderer.update_map(player_x, player_y, ' ')
                
                # Update player position
                player_x, player_y = new_x, new_y
                await renderer.update_map(player_x, player_y, '@')
        
        # Small delay to prevent too rapid updates
        await asyncio.sleep(0.01)

if __name__ == "__main__":
    # Run the async game loop
    from renderer import AsyncMapRenderer
    from assets.reader import get_gui, get_gui_properties, get_player
    asyncio.run(main_game_loop())