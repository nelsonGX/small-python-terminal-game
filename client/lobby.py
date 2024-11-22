import os
import asyncio
import signal
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Set
from enum import Enum, auto
from dataclasses import dataclass, asdict

class GameMode(Enum):
    PVE = "PvE"
    PVP = "PvP"
    COOP = "Co-op"

@dataclass
class Player:
    id: str
    name: str
    level: int
    character_class: str
    ready: bool = False
    room_id: Optional[str] = None

@dataclass
class GameRoom:
    id: str
    name: str
    host_id: str
    mode: GameMode
    max_players: int
    min_level: int
    max_level: int
    password: Optional[str]
    created_at: str
    players: Set[str]  # Set of player IDs
    status: str = "WAITING"  # WAITING, FULL, IN_GAME

class LobbyState(Enum):
    MAIN_MENU = auto()
    ROOM_LIST = auto()
    ROOM_CREATE = auto()
    IN_ROOM = auto()
    LOADING = auto()

class MultiplayerLobby:
    def __init__(self):
        self.state = LobbyState.MAIN_MENU
        self.rooms: Dict[str, GameRoom] = {}
        self.players: Dict[str, Player] = {}
        self.current_player: Optional[Player] = None
        self.current_room: Optional[GameRoom] = None
        self.running = True
        self.selected_index = 0
        self.error_message: Optional[str] = None
        self.success_message: Optional[str] = None

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def create_test_data(self):
        """Create some test rooms and players for demonstration"""
        # Create test players
        players = [
            Player(str(uuid.uuid4()), "Gandalf", 50, "Wizard"),
            Player(str(uuid.uuid4()), "Aragorn", 45, "Warrior"),
            Player(str(uuid.uuid4()), "Legolas", 43, "Archer"),
            Player(str(uuid.uuid4()), "Gimli", 42, "Warrior")
        ]
        for player in players:
            self.players[player.id] = player

        # Create test rooms
        rooms = [
            GameRoom(
                id=str(uuid.uuid4()),
                name="Dragon Hunt",
                host_id=players[0].id,
                mode=GameMode.PVE,
                max_players=4,
                min_level=40,
                max_level=50,
                password=None,
                created_at=datetime.now().isoformat(),
                players={players[0].id}
            ),
            GameRoom(
                id=str(uuid.uuid4()),
                name="PvP Arena",
                host_id=players[1].id,
                mode=GameMode.PVP,
                max_players=8,
                min_level=30,
                max_level=60,
                password="battle",
                created_at=datetime.now().isoformat(),
                players={players[1].id, players[2].id}
            )
        ]
        for room in rooms:
            self.rooms[room.id] = room

    def draw_header(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    EPIC RPG MULTIPLAYER                      ║
╚══════════════════════════════════════════════════════════════╝
        """)

    def draw_player_info(self):
        if self.current_player:
            p = self.current_player
            print(f"""
╔══════════════ Player Info ══════════════╗
║ Name: {p.name:<32} ║
║ Level: {p.level:<31} ║
║ Class: {p.character_class:<31} ║
╚═══════════════════════════════════════════╝
            """)

    def draw_room_list(self):
        print("\n╔══════════════ Available Rooms ══════════════╗")
        print("║ ID | Name         | Mode | Players | Level  ║")
        print("╠════════════════════════════════════════════╣")
        
        sorted_rooms = sorted(self.rooms.values(), key=lambda r: r.created_at, reverse=True)
        for idx, room in enumerate(sorted_rooms):
            players_count = len(room.players)
            cursor = ">" if idx == self.selected_index else " "
            print(f"║{cursor}{room.id[:3]} | {room.name:<12} | {room.mode.value:<4} | {players_count}/{room.max_players:<2} | {room.min_level}-{room.max_level:<2} ║")
        
        print("╚════════════════════════════════════════════╝")

    def draw_room_details(self, room: GameRoom):
        print(f"""
╔══════════════ Room Details ══════════════╗
║ Name: {room.name:<32} ║
║ Mode: {room.mode.value:<32} ║
║ Players: {len(room.players)}/{room.max_players:<29} ║
║ Level Range: {room.min_level}-{room.max_level:<26} ║
║ Status: {room.status:<31} ║
║ Password Protected: {'Yes' if room.password else 'No':<23} ║
╠══════════════ Players ══════════════════╣""")
        
        for player_id in room.players:
            player = self.players.get(player_id)
            if player:
                ready_status = "[Ready]" if player.ready else "[Not Ready]"
                host_status = "[Host]" if player_id == room.host_id else " " * 6
                print(f"║ {player.name:<15} | Lvl {player.level:<3} | {player.character_class:<8} | {ready_status} {host_status} ║")
        
        print("╚═══════════════════════════════════════════╝")

    async def create_room(self):
        self.clear_screen()
        self.draw_header()
        print("\nCreate New Room")
        print("==============")
        
        try:
            room_name = input("Room Name: ")
            max_players = int(input("Max Players (2-8): "))
            min_level = int(input("Minimum Level: "))
            max_level = int(input("Maximum Level: "))
            
            print("\nSelect Game Mode:")
            for idx, mode in enumerate(GameMode):
                print(f"{idx + 1}. {mode.value}")
            mode_choice = int(input("Choice: "))
            mode = list(GameMode)[mode_choice - 1]
            
            password = input("Room Password (optional): ").strip() or None
            
            room = GameRoom(
                id=str(uuid.uuid4()),
                name=room_name,
                host_id=self.current_player.id,
                mode=mode,
                max_players=max_players,
                min_level=min_level,
                max_level=max_level,
                password=password,
                created_at=datetime.now().isoformat(),
                players={self.current_player.id}
            )
            
            self.rooms[room.id] = room
            self.current_room = room
            self.state = LobbyState.IN_ROOM
            self.success_message = "Room created successfully!"
            
        except ValueError as e:
            self.error_message = "Invalid input. Please try again."
            await asyncio.sleep(2)
            self.error_message = None

    async def join_room(self, room_id: str):
        room = self.rooms.get(room_id)
        if not room:
            self.error_message = "Room not found!"
            return

        if len(room.players) >= room.max_players:
            self.error_message = "Room is full!"
            return

        if self.current_player.level < room.min_level or self.current_player.level > room.max_level:
            self.error_message = f"Your level ({self.current_player.level}) is not within the room's range ({room.min_level}-{room.max_level})"
            return

        if room.password:
            password = input("Enter room password: ")
            if password != room.password:
                self.error_message = "Incorrect password!"
                return

        room.players.add(self.current_player.id)
        self.current_player.room_id = room.id
        self.current_room = room
        self.state = LobbyState.IN_ROOM
        self.success_message = "Joined room successfully!"

    async def leave_room(self):
        if not self.current_room:
            return

        self.current_room.players.remove(self.current_player.id)
        
        # If room is empty, remove it
        if not self.current_room.players:
            del self.rooms[self.current_room.id]
        # If leaving player was host, assign new host
        elif self.current_room.host_id == self.current_player.id:
            self.current_room.host_id = next(iter(self.current_room.players))

        self.current_player.room_id = None
        self.current_player.ready = False
        self.current_room = None
        self.state = LobbyState.ROOM_LIST
        self.success_message = "Left room successfully!"

    async def toggle_ready(self):
        if self.current_room and self.current_player:
            self.current_player.ready = not self.current_player.ready
            
            # Check if all players are ready
            if all(self.players[pid].ready for pid in self.current_room.players):
                self.current_room.status = "STARTING"
                # Here you would typically start a countdown and transition to the game

    async def handle_input(self):
        if os.name == 'nt':  # Windows
            import msvcrt
            while self.running:
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    await self.process_key_input(key)
                await asyncio.sleep(0.01)
        else:  # Unix-like
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                while self.running:
                    if select.select([sys.stdin], [], [], 0)[0]:
                        ch = sys.stdin.read(1)
                        await self.process_unix_input(ch)
                    await asyncio.sleep(0.01)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    async def process_key_input(self, key: bytes):
        if self.state == LobbyState.ROOM_LIST:
            if key == b'\xe0':  # Special key prefix
                key = msvcrt.getch()
                if key == b'H':  # Up arrow
                    self.selected_index = max(0, self.selected_index - 1)
                elif key == b'P':  # Down arrow
                    self.selected_index = min(len(self.rooms) - 1, self.selected_index + 1)
            elif key == b'\r':  # Enter
                if self.rooms:
                    room_id = list(self.rooms.keys())[self.selected_index]
                    await self.join_room(room_id)
            elif key == b'c':  # Create room
                self.state = LobbyState.ROOM_CREATE
                await self.create_room()

    async def process_unix_input(self, ch: str):
        if ch == '\x1b':
            next1, next2 = sys.stdin.read(2)
            if next1 == '[':
                if next2 == 'A':  # Up arrow
                    self.selected_index = max(0, self.selected_index - 1)
                elif next2 == 'B':  # Down arrow
                    self.selected_index = min(len(self.rooms) - 1, self.selected_index + 1)
        elif ch == '\r':  # Enter
            if self.rooms:
                room_id = list(self.rooms.keys())[self.selected_index]
                await self.join_room(room_id)
        elif ch == 'c':  # Create room
            self.state = LobbyState.ROOM_CREATE
            await self.create_room()

    async def update_display(self):
        while self.running:
            self.clear_screen()
            self.draw_header()
            self.draw_player_info()

            if self.error_message:
                print(f"\nError: {self.error_message}")
            if self.success_message:
                print(f"\nSuccess: {self.success_message}")

            if self.state == LobbyState.ROOM_LIST:
                self.draw_room_list()
                print("\nControls:")
                print("↑↓: Navigate | Enter: Join Room | C: Create Room | Q: Quit")
            elif self.state == LobbyState.IN_ROOM:
                if self.current_room:
                    self.draw_room_details(self.current_room)
                    print("\nControls:")
                    print("R: Ready/Unready | L: Leave Room | Q: Quit")

            await asyncio.sleep(0.1)

    async def run(self):
        # Create test data
        self.create_test_data()
        
        # Set current player (in a real game, this would come from login)
        self.current_player = Player(
            id=str(uuid.uuid4()),
            name="NewPlayer",
            level=40,
            character_class="Warrior"
        )
        self.players[self.current_player.id] = self.current_player
        
        # Set initial state
        self.state = LobbyState.ROOM_LIST

        # Start main tasks
        tasks = [
            asyncio.create_task(self.update_display()),
            asyncio.create_task(self.handle_input())
        ]

        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            for task in tasks:
                task.cancel()

if __name__ == "__main__":
    # Import platform-specific modules
    if os.name == 'nt':
        import msvcrt
    else:
        import select

    # Create and run the lobby
    lobby = MultiplayerLobby()
    asyncio.run(lobby.run())