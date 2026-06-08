"""
Menu System Module
Handles game menus and UI navigation.
"""

import pygame
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class MenuAction(Enum):
    """Possible menu actions"""
    START_GAME = 1
    CHANGE_LOCATION = 2
    QUIT = 3
    OPEN_SETTINGS = 4


@dataclass
class MenuItem:
    """Single menu item definition"""
    text: str
    action: MenuAction
    metadata: Optional[Dict] = None
    color: Tuple[int, int, int] = (255, 255, 255)
    selected_color: Tuple[int, int, int] = (255, 0, 0)


class MenuSystem:
    """
    Game menu system with navigation and selection.

    Attributes:
        items (List[MenuItem]): Available menu options
        current_selection (int): Index of selected item
        font (pygame.font.Font): Menu font
    """

    def __init__(self, title: str, items: List[MenuItem]):
        self.title = title
        self.items = items
        self.current_selection = 0
        self.font = pygame.font.SysFont('Arial', 36)
        self.title_font = pygame.font.SysFont('Arial', 48, bold=True)

    def handle_input(self, event: pygame.event.Event) -> Optional[MenuItem]:
        """Process user input for menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.current_selection = (self.current_selection + 1) % len(self.items)
            elif event.key == pygame.K_UP:
                self.current_selection = (self.current_selection - 1) % len(self.items)
            elif event.key == pygame.K_RETURN:
                return self.items[self.current_selection]
        return None

    def draw(self, surface: pygame.Surface) -> None:
        """Render menu to surface"""
        # Draw title
        title_surf = self.title_font.render(self.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(surface.get_width() // 2, 100))
        surface.blit(title_surf, title_rect)

        # Draw menu items
        for i, item in enumerate(self.items):
            color = item.selected_color if i == self.current_selection else item.color
            item_surf = self.font.render(item.text, True, color)
            item_rect = item_surf.get_rect(center=(surface.get_width() // 2, 200 + i * 50))
            surface.blit(item_surf, item_rect)