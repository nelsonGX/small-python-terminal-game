import random
import time
import os
import math
from typing import List, Tuple

class Dice3D:
    def __init__(self, size: int = 20):
        self.size = size
        self.screen_width = 60
        self.screen_height = 30
        self.faces = self._create_faces()
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0
        self.chars = "░▒▓█"

    def _create_faces(self) -> dict:
        faces = {}
        # Face patterns (centered dots for each number)
        patterns = {
            1: [(1/2, 1/2)],
            2: [(1/3, 1/3), (2/3, 2/3)],
            3: [(1/3, 1/3), (1/2, 1/2), (2/3, 2/3)],
            4: [(1/3, 1/3), (2/3, 1/3), (1/3, 2/3), (2/3, 2/3)],
            5: [(1/3, 1/3), (2/3, 1/3), (1/2, 1/2), (1/3, 2/3), (2/3, 2/3)],
            6: [(1/3, 1/3), (2/3, 1/3), (1/3, 1/2), (2/3, 1/2), (1/3, 2/3), (2/3, 2/3)]
        }
        
        for number, pattern in patterns.items():
            face = [[' ' for _ in range(self.size)] for _ in range(self.size)]
            for px, py in pattern:
                x = int(px * (self.size - 1))
                y = int(py * (self.size - 1))
                face[y][x] = '●'
            faces[number] = face
        return faces

    def _create_buffer(self) -> List[List[str]]:
        return [[' ' for _ in range(self.screen_width)] for _ in range(self.screen_height)]

    def _rotate_point(self, point: Tuple[float, float, float], scale: float = 1.0) -> Tuple[float, float, float]:
        x, y, z = [coord * scale for coord in point]
        
        # Rotate around X axis
        y2 = y * math.cos(self.angle_x) - z * math.sin(self.angle_x)
        z2 = y * math.sin(self.angle_x) + z * math.cos(self.angle_x)
        
        # Rotate around Y axis
        x3 = x * math.cos(self.angle_y) + z2 * math.sin(self.angle_y)
        z3 = -x * math.sin(self.angle_y) + z2 * math.cos(self.angle_y)
        
        # Rotate around Z axis
        x4 = x3 * math.cos(self.angle_z) - y2 * math.sin(self.angle_z)
        y4 = x3 * math.sin(self.angle_z) + y2 * math.cos(self.angle_z)
        
        return (x4, y4, z3)

    def _project_point(self, point: Tuple[float, float, float], x_offset: float = 0) -> Tuple[int, int]:
        x, y, z = point
        scale = 15
        z_offset = 5
        x_proj = int((x + x_offset) * scale / (z + z_offset) + self.screen_width // 2)
        y_proj = int(y * scale / (z + z_offset) + self.screen_height // 2)
        return (x_proj, y_proj)

    def _draw_line(self, buffer: List[List[str]], start: Tuple[int, int], end: Tuple[int, int], char: str):
        x1, y1 = start
        x2, y2 = end
        
        if (x1 < 0 or x1 >= self.screen_width or y1 < 0 or y1 >= self.screen_height or
            x2 < 0 or x2 >= self.screen_width or y2 < 0 or y2 >= self.screen_height):
            return

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        steep = dy > dx

        if steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = abs(y2 - y1)
        error = dx // 2
        y = y1
        y_step = 1 if y1 < y2 else -1

        for x in range(x1, x2 + 1):
            if steep:
                if 0 <= y < self.screen_width and 0 <= x < self.screen_height:
                    buffer[x][y] = char
            else:
                if 0 <= x < self.screen_width and 0 <= y < self.screen_height:
                    buffer[y][x] = char
            error -= dy
            if error < 0:
                y += y_step
                error += dx

    def _clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def _apply_physics(self):
        # Apply friction
        friction = 0.98
        self.velocity_x *= friction
        self.velocity_y *= friction
        self.velocity_z *= friction
        
        # Update angles
        self.angle_x += self.velocity_x
        self.angle_y += self.velocity_y
        self.angle_z += self.velocity_z

    def roll(self, num_frames: int = 45):
        result = random.randint(1, 6)
        
        # Initial velocities
        self.velocity_x = random.uniform(-0.3, 0.3)
        self.velocity_y = random.uniform(-0.3, 0.3)
        self.velocity_z = random.uniform(-0.3, 0.3)
        
        # Pop-in and slide animation parameters
        pop_frames = 15
        initial_scale = 0.1
        initial_x_offset = -20  # Start far to the left
        
        vertices = [
            (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
            (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)
        ]
        
        edges = [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ]

        faces = [
            (0, 1, 2, 3), (4, 5, 6, 7),
            (0, 1, 5, 4), (2, 3, 7, 6),
            (0, 3, 7, 4), (1, 2, 6, 5)
        ]
        
        for frame in range(num_frames):
            self._apply_physics()
            buffer = self._create_buffer()
            
            # Calculate scale and position for pop-in effect
            if frame < pop_frames:
                progress = frame / pop_frames
                # Smooth easing function for better animation
                ease_progress = 1 - math.cos(progress * math.pi / 2)
                
                current_scale = initial_scale + (1 - initial_scale) * ease_progress
                # Add a slight bouncy effect using sine
                bounce_factor = math.sin(progress * math.pi / 2)
                current_scale *= 1 + 0.1 * bounce_factor
                
                # Calculate x offset with easing
                x_offset = initial_x_offset * (1 - ease_progress)
                
                # Add a slight vertical bounce
                y_bounce = math.sin(progress * math.pi) * 0.5
                self.angle_x = y_bounce
            else:
                current_scale = 1.0
                x_offset = 0
            
            # Calculate z-order for faces
            face_depths = []
            for face in faces:
                points = [self._rotate_point(vertices[i], current_scale) for i in face]
                avg_z = sum(p[2] for p in points) / len(points)
                face_depths.append((face, avg_z, points))
            
            # Sort faces by depth
            face_depths.sort(key=lambda x: x[1], reverse=True)
            
            # Draw faces and edges
            for face, _, points in face_depths:
                projected = [self._project_point(p, x_offset) for p in points]
                
                # Draw face edges
                for i in range(len(projected)):
                    self._draw_line(buffer, projected[i], projected[(i + 1) % len(projected)], '█')
            
            # Display frame
            self._clear_screen()
            print('\n'.join(''.join(row) for row in buffer))
            time.sleep(0.04)
        
        # Show final result
        return result

if __name__ == "__main__":
    dice = Dice3D()
    dice.roll()