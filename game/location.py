from dataclasses import dataclass
import pygame

@dataclass
class LocationRules:
    speed_modifier: float = 1.0
    food_value: int = 1
    snake_color: tuple = (0, 255, 0)
    special_effect: str = None

class Location:
    def __init__(self, width=800, height=600, block_size=20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.obstacles = []
        self.rules = LocationRules()
        self.background = None

    def draw(self, surface):
        """Draw location background"""
        if self.background:
            surface.blit(self.background, (0, 0))