import pygame
from ..location import Location, LocationRules

class CrossroadsLocation(Location):
    def __init__(self, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=1.0,
            food_value=1,
            snake_color=(64, 224, 208)  # Turquoise color
        )
        self.obstacles = []  # No obstacles
        self.background = pygame.Surface((width, height))
        self.background.fill((0, 0, 0))
        self.portal_rect = pygame.Rect(width - 40, height - 40, 30, 30)
        self.portal_active = False