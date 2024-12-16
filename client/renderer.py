import asyncio

class AsyncMapRenderer:
    def __init__(self, map_content, viewport_width=80, viewport_height=24):
        """
        Initialize the async map renderer with the map content and viewport dimensions.
        
        Args:
            map_content (str): The initial map content as a multi-line string
            viewport_width (int): Width of the visible area
            viewport_height (int): Height of the visible area
        """
        self.map_lines = map_content.split('\n')
        self.map_height = len(self.map_lines)
        self.map_width = max(len(line) for line in self.map_lines)
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        
        # Normalize map width by padding shorter lines
        self.map_lines = [line.ljust(self.map_width) for line in self.map_lines]

    async def get_viewport(self, player_x, player_y):
        """
        Asynchronously get the visible portion of the map centered around the player.
        
        Args:
            player_x (int): Player's x coordinate in the map
            player_y (int): Player's y coordinate in the map
            
        Returns:
            str: The visible portion of the map as a multi-line string
        """
        # Calculate viewport boundaries
        start_x = max(0, player_x - self.viewport_width // 2)
        start_y = max(0, player_y - self.viewport_height // 2)
        end_x = min(self.map_width, start_x + self.viewport_width)
        end_y = min(self.map_height, start_y + self.viewport_height)
        
        # Extract visible portion of the map
        visible_lines = []
        for y in range(start_y, end_y):
            line = self.map_lines[y][start_x:end_x]
            visible_lines.append(line)
            await asyncio.sleep(0)  # Allow other tasks to run
        
        # Add padding if viewport is not completely filled
        while len(visible_lines) < self.viewport_height:
            visible_lines.append(' ' * (end_x - start_x))
            
        for i in range(len(visible_lines)):
            if len(visible_lines[i]) < self.viewport_width:
                visible_lines[i] = visible_lines[i].ljust(self.viewport_width)
        
        return '\n'.join(visible_lines)

    async def update_map(self, x, y, tile):
        """
        Asynchronously update a specific tile in the map.
        
        Args:
            x (int): X coordinate to update
            y (int): Y coordinate to update
            tile (str): Single character to place at the specified position
        """
        if 0 <= y < self.map_height and 0 <= x < self.map_width:
            line = list(self.map_lines[y])
            line[x] = tile
            self.map_lines[y] = ''.join(line)
            await asyncio.sleep(0)  # Allow other tasks to run