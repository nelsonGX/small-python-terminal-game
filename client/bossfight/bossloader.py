import os
import time
import shutil

from client.assets.reader import get_gui
# from ..assets.reader import get_gui

# ASCII art texts
text1 = get_gui("boss").strip().split('\n')

text2 = get_gui("fight").strip().split('\n')

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_text_width(text_lines):
    """Get the maximum width of the text."""
    return max(len(line) for line in text_lines)

def create_frame(text1_lines, text2_lines, text1_pos, text2_pos):
    """Create a single frame of the animation."""
    text1_width = get_text_width(text1_lines)
    text2_width = get_text_width(text2_lines)
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

def main():
    text1_width = get_text_width(text1)
    text2_width = get_text_width(text2)
    
    # Starting positions
    text1_pos = 20  # Start from right edge
    text2_pos = -text2_width    # Start from left edge (negative)
    
    # Target positions
    text1_target = 0  # Left align
    text2_target = 10  # 5 spaces indent
    
    # Animation speed (lower is faster)
    speed = 0.08
    
    # Main animation loop
    while text1_pos > text1_target or text2_pos < text2_target:
        clear_screen()
        
        # Update positions
        if text1_pos > text1_target:
            text1_pos -= 2
        if text2_pos < text2_target:
            text2_pos += 2
        
        # Ensure we don't overshoot targets
        text1_pos = max(text1_pos, text1_target)
        text2_pos = min(text2_pos, text2_target)
        
        # Create and display frame
        frame = create_frame(text1, text2, text1_pos, text2_pos)
        print('\n'.join(frame))
        
        time.sleep(speed)
    
    # Ensure final frame is displayed
    clear_screen()
    final_frame = create_frame(text1, text2, text1_target, text2_target)
    print('\n'.join(final_frame))

if __name__ == "__main__":
    main()