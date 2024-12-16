import random
import asyncio
import os
import math
from client.assets.reader import get_gui

async def clear_screen():
    # Cross-platform clear screen
    os.system('cls' if os.name == 'nt' else 'clear')

loading_bar = """------------------------
|%%%%%%%%%%%%%%%%%%%%%%|
------------------------
"""

loading_content = "▇"

async def loading(title):
    logo = await get_gui("title")
    os.system("clear")
    max_size = loading_bar.count("%")
    for i in range(max_size + 1):
        print(logo)
        print(title)
        print(loading_bar.replace("%", loading_content * i, 1).replace("%", " " * (max_size - i), 1).replace("%", ""), end="")
        await asyncio.sleep(random.uniform(0.01, 0.05))
        await clear_screen()
    print("Loaded!")

async def transition():
    async def generate_fog_frame(size_x, size_y, progress):
        # Create a 50x50 frame with a dissipating fog effect
        frame = []
        for y in range(size_y):
            row = ""
            for x in range(size_x):
                # Create noise pattern with dissipation based on progress
                noise = random.random()
                
                # Fog density decreases as progress increases
                density = 1 - progress
                
                # Add some swirling effect
                swirl = math.sin((x + y)/10 + progress * 6) * 0.2
                
                # Combine noise and swirl with progress-based dissipation
                value = noise * density + swirl
                
                # Use different characters for fog density
                if value > 0.8:
                    char = "█"  # Dense fog
                elif value > 0.6:
                    char = "▓"  # Medium-heavy fog
                elif value > 0.4:
                    char = "▒"  # Medium-light fog
                elif value > 0.2:
                    char = "░"  # Light fog
                else:
                    char = " "  # Clear space
                
                row += char
            frame.append(row)
        return frame

    async def display_frame(frame):
        # Display the frame
        for row in frame:
            print(row)

    async def animate():
        size_x = 50
        size_y = 30
        duration = 0.5  # Animation duration in seconds
        fps = 30  # Frames per second
        total_frames = int(duration * fps)
        frame_duration = 1.0 / fps

        try:
            for frame_num in range(total_frames):
                await clear_screen()
                # Use a smoothed progress curve for more natural dissipation
                progress = (frame_num / total_frames) ** 0.8  # Adjusted power for smoother dissipation
                frame = await generate_fog_frame(size_x, size_y, progress)
                await display_frame(frame)
                await asyncio.sleep(frame_duration)
        except KeyboardInterrupt:
            print("\nAnimation stopped by user")

    async def main():
        # Set random seed for consistent fog pattern
        random.seed(42)
        
        # Create animation task
        animation_task = asyncio.create_task(animate())
        
        # Wait for animation to complete
        await animation_task

    await main()

# testing
if __name__ == "__main__":
    asyncio.run(transition())