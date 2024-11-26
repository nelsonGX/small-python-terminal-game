import os
import asyncio
import signal
import sys
from typing import List, Tuple, Optional
from enum import Enum, auto

class GameState(Enum):
    MENU = auto()
    LOADING = auto()
    IN_GAME = auto()
    SETTINGS = auto()
    CHARACTER_CREATION = auto()
    EXIT = auto()

class AsyncLobbyGUI:
    def __init__(self):
        self.title = """╔══════════════════════════════════════════╗
║             EPIC RPG ADVENTURE           ║
╚══════════════════════════════════════════╝"""
        
        self.menu_options = [
            "1. Start New Game",
            "2. Load Game",
            "3. Character Creation",
            "4. Settings",
            "5. Credits",
            "6. Exit"
        ]
        self.selected_option = 0
        self.state = GameState.MENU
        self.running = True
        self.loading_task: Optional[asyncio.Task] = None
        self.background_tasks: List[asyncio.Task] = []
        self.last_drawn_option = -1
        self.cursor_position = 0
        self._terminal_settings = None

    def setup_terminal(self):
        """Set up terminal for raw input mode"""
        if os.name == 'nt':  # Windows
            import msvcrt
            # Enable ANSI escape sequences on Windows
            from ctypes import windll
            kernel32 = windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        else:  # Unix-like
            import termios
            import tty
            self._terminal_settings = termios.tcgetattr(sys.stdin.fileno())
            tty.setraw(sys.stdin.fileno())
            sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

    def restore_terminal(self):
        """Restore terminal to original settings"""
        if os.name != 'nt' and self._terminal_settings:
            import termios
            termios.tcsetattr(
                sys.stdin.fileno(),
                termios.TCSADRAIN,
                self._terminal_settings
            )

    async def initial_draw(self):
        """Initial full draw of the interface"""
        # Clear screen and move to top-left
        print("\033[2J\033[H", end='', flush=True)
        
        # Print title
        print(self.title, end='\n', flush=True)
        
        # Print character preview
        preview = [
            "           /\\",
            "          /  \\",
            "         /    \\",
            "        /      \\",
            "       |   ○  ○ |",
            "       |    ◡   |",
            "        \\  --  /",
            "         \\    /",
            "          \\  /",
            "           \\/"
        ]
        for line in preview:
            print(line, flush=True)
        
        # Print menu frame
        print("\n╔══════════════ MENU ══════════════╗", flush=True)
        
        # Print menu options
        for idx, option in enumerate(self.menu_options):
            if idx == self.selected_option:
                print(f"║ > {option:<28} ║", flush=True)
            else:
                print(f"║   {option:<28} ║", flush=True)
        
        print("╚════════════════════════════════════╝", flush=True)
        print("\nUse ↑↓ arrows to navigate and Enter to select", flush=True)
        
        # Calculate and store cursor position for later use
        self.cursor_position = len(self.menu_options) + 4
        sys.stdout.flush()
        
        # Move cursor back up to the first menu option
        print(f"\033[{self.cursor_position}A", end='', flush=True)
        sys.stdout.flush()

    def update_selected_option(self):
        """Update only the changed menu option lines"""
        if self.last_drawn_option != self.selected_option:
            # Move to and clear previous selection
            if self.last_drawn_option >= 0:
                print(f"\033[{self.last_drawn_option}B", end='', flush=True)
                print(f"║   {self.menu_options[self.last_drawn_option]:<28} ║", end='', flush=True)
            
            # Move to and update new selection
            moves = self.selected_option - (self.last_drawn_option if self.last_drawn_option >= 0 else 0)
            if moves != 0:
                print(f"\033[{abs(moves)}{'B' if moves > 0 else 'A'}", end='', flush=True)
            print(f"║ > {self.menu_options[self.selected_option]:<28} ║", end='', flush=True)
            
            # Return cursor to menu start
            print(f"\033[{self.selected_option}A", end='', flush=True)
            
            self.last_drawn_option = self.selected_option
            sys.stdout.flush()

    async def loading_animation(self) -> None:
        animations = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        try:
            # Move cursor to bottom of menu
            print(f"\033[{self.cursor_position + 2}B", end='', flush=True)
            while self.state == GameState.LOADING:
                for frame in animations:
                    if self.state != GameState.LOADING:
                        break
                    print(f"\rLoading {frame}", end="", flush=True)
                    await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print("\rLoaded!    ")
        finally:
            # Return cursor to menu position
            print(f"\033[{self.cursor_position + 2}A", end='', flush=True)

    async def background_state_update(self) -> None:
        """Simulates background game state updates"""
        try:
            while self.running:
                await asyncio.sleep(1)
                # Add background tasks here (e.g., autosave, network sync, etc.)
        except asyncio.CancelledError:
            pass

    async def handle_input(self) -> None:
        try:
            if os.name == 'nt':  # Windows
                import msvcrt
                while self.running:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                        await self.process_key_input(key)
                    await asyncio.sleep(0.01)
            else:  # Unix-like
                import sys
                reader = asyncio.StreamReader()
                protocol = asyncio.StreamReaderProtocol(reader)
                await asyncio.get_event_loop().connect_read_pipe(
                    lambda: protocol, sys.stdin)

                while self.running:
                    ch = await reader.read(1)
                    if ch == b'\x1b':
                        seq = await reader.read(2)
                        if seq == b'[A':  # Up arrow
                            self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                            self.update_selected_option()
                        elif seq == b'[B':  # Down arrow
                            self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                            self.update_selected_option()
                    elif ch == b'\r':  # Enter key
                        await self.handle_selection(self.menu_options[self.selected_option].split(". ")[1])
        except Exception as e:
            self.restore_terminal()
            raise e

    async def process_key_input(self, key: bytes) -> None:
        if key == b'\xe0':  # Special key prefix
            import msvcrt
            key = msvcrt.getch()
            if key == b'H':  # Up arrow
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
                self.update_selected_option()
            elif key == b'P':  # Down arrow
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
                self.update_selected_option()
        elif key == b'\r':  # Enter key
            await self.handle_selection(self.menu_options[self.selected_option].split(". ")[1])

    async def handle_selection(self, selection: str) -> None:
        self.state = GameState.LOADING
        self.loading_task = asyncio.create_task(self.loading_animation())
        
        # Simulate some loading time
        await asyncio.sleep(2)
        
        if self.loading_task:
            self.loading_task.cancel()
            try:
                await self.loading_task
            except asyncio.CancelledError:
                pass

        if selection == "Exit":
            self.running = False
            self.state = GameState.EXIT
            print(f"\033[{self.cursor_position + 2}B", end='', flush=True)
            print("\nThanks for playing!")
            return

        elif selection == "Start New Game":
            self.state = GameState.IN_GAME
            print(f"\033[{self.cursor_position + 2}B", end='', flush=True)
            print("\nStarting new game...")
            
        elif selection == "Character Creation":
            self.state = GameState.CHARACTER_CREATION
            print(f"\033[{self.cursor_position + 2}B", end='', flush=True)
            print("\nEntering character creation...")
            
        elif selection == "Settings":
            self.state = GameState.SETTINGS
            print(f"\033[{self.cursor_position + 2}B", end='', flush=True)
            print("\nOpening settings...")
            
        await asyncio.sleep(1)
        self.state = GameState.MENU
        print(f"\033[{self.cursor_position + 2}A", end='', flush=True)

    async def run(self):
        """Main run loop"""
        # Set up terminal
        self.setup_terminal()

        try:
            # Set up signal handlers
            signal.signal(signal.SIGINT, lambda s, f: self.handle_signal(s, f))
            signal.signal(signal.SIGTERM, lambda s, f: self.handle_signal(s, f))

            # Initial draw
            await self.initial_draw()

            # Create background tasks
            self.background_tasks = [
                asyncio.create_task(self.background_state_update()),
                asyncio.create_task(self.handle_input())
            ]

            # Wait for tasks to complete
            await asyncio.gather(*self.background_tasks, return_exceptions=True)

        finally:
            # Cleanup
            self.restore_terminal()
            for task in self.background_tasks:
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass

    def handle_signal(self, signum, frame):
        """Handle system signals for clean shutdown"""
        self.running = False
        self.restore_terminal()
        for task in self.background_tasks:
            task.cancel()

async def entry():
    # Ensure proper terminal initialization
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    
    # Create and run the lobby
    lobby = AsyncLobbyGUI()
    try:
        await lobby.run()
    finally:
        lobby.restore_terminal()
        # Move cursor to bottom of screen
        print("\033[?25h", end='', flush=True)  # Show cursor
        print("\n" * 2, end='', flush=True)  # Add some padding at the bottom