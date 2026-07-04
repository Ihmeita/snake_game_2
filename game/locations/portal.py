import pygame
from ..location import Location, LocationRules

class PortalLocation(Location):
    def __init__(self, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=1.0,
            food_value=1,
            snake_color=(0, 0, 0)  # Black color
        )
        self.obstacles = []
        self.background = pygame.Surface((width, height))
        self.background.fill((235, 228, 215))
        self.portal_rect = pygame.Rect(10, 10, 30, 30)
