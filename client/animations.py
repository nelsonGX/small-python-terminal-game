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


async def load_boss(speed=0.05):
    # ASCII art texts
    async def get_text():
        text1 = await get_gui("boss")
        text2 = await get_gui("fight")

        text1 = text1.strip().split('\n')
        text2 = text2.strip().split('\n')
        return text1, text2

    async def get_text_width(text_lines):
        """Get the maximum width of the text."""
        return max(len(line) for line in text_lines)

    async def create_frame(text1_lines, text2_lines, text1_pos, text2_pos):
        """Create a single frame of the animation."""
        text1_width = await get_text_width(text1_lines)
        text2_width = await get_text_width(text2_lines)
        frame = []
        
        # Add text1
        for line in text1_lines:
            # Pad the line with spaces to match the maximum width
            padded_line = line.ljust(text1_width)
            # Add spaces before the text based on position
            frame_line = " " * text1_pos + padded_line
            frame.append(frame_line)
        
        # Add spacing between texts
        frame.append("")  # Empty line for separation
        
        # Add text2
        for line in text2_lines:
            padded_line = line.ljust(text2_width)
            frame_line = " " * text2_pos + padded_line
            frame.append(frame_line)
        
        return frame
    text1, text2 = await get_text()
    
    # Starting positions
    text1_pos = 20
    text2_pos = 0
    
    # Target positions
    text1_target = 0  # Left align
    text2_target = 15  # 5 spaces indent

    # Main animation loop
    while text1_pos > text1_target:
        await clear_screen()
        text1_pos -= 2
        text1_pos = max(text1_pos, text1_target)
        
        # Create and display frame
        frame = await create_frame(text1, text2, text1_pos, text2_pos)
        print('\n'.join(frame))
        await asyncio.sleep(speed)
    
    # Second phase: Animate text2
    while text2_pos < text2_target:
        await clear_screen()
        text2_pos += 2
        text2_pos = min(text2_pos, text2_target)
        
        # Create and display frame
        frame = await create_frame(text1, text2, text1_pos, text2_pos)
        print('\n'.join(frame))
        await asyncio.sleep(speed)
    
    # Ensure final frame is displayed
    await clear_screen()
    final_frame = await create_frame(text1, text2, text1_target, text2_target)
    print('\n'.join(final_frame))

# testing
if __name__ == "__main__":
    asyncio.run(transition())