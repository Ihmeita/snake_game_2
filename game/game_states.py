"""
Game State Management
Handles transitions between different game states.
"""

from enum import Enum, auto
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .menu import MenuSystem, MenuItem, MenuAction
import pygame


class GameState(Enum):
    """All possible game states"""
    MAIN_MENU = auto()
    LOCATION_SELECT = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()


@dataclass
class GameContext:
    """Shared game data between states"""
    current_location: Optional[str] = None
    player_score: int = 0
    high_score: int = 0
    settings: Dict[str, Any] = None


class StateManager:
    """
    Finite state machine for game flow control.

    Args:
        screen: Pygame display surface
    """

    def __init__(self, screen):
        self.screen = screen
        self.current_state = GameState.MAIN_MENU
        self.context = GameContext()
        self._init_states()

    def _init_states(self) -> None:
        """Initialize all state handlers"""
        self.states = {
            GameState.MAIN_MENU: self._main_menu_state,
            GameState.LOCATION_SELECT: self._location_select_state,
            GameState.PLAYING: self._playing_state
        }

        # Main menu configuration
        self.main_menu = MenuSystem(
            "Snake Game",
            [
                MenuItem("Start Game", MenuAction.START_GAME),
                MenuItem("Select Location", MenuAction.CHANGE_LOCATION),
                MenuItem("Settings", MenuAction.OPEN_SETTINGS),
                MenuItem("Quit", MenuAction.QUIT)
            ]
        )

    def _main_menu_state(self, event: pygame.event.Event) -> None:
        """Handle main menu state"""
        selected_item = self.main_menu.handle_input(event)
        self.main_menu.draw(self.screen)

        if selected_item:
            if selected_item.action == MenuAction.START_GAME:
                self.current_state = GameState.PLAYING
            elif selected_item.action == MenuAction.CHANGE_LOCATION:
                self.current_state = GameState.LOCATION_SELECT

    def run(self) -> None:
        """Main state machine loop"""
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Delegate to current state handler
                if self.current_state in self.states:
                    self.states[self.current_state](event)

            pygame.display.flip()
            clock.tick(60)