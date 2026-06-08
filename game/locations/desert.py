"""
Desert Location Implementation
"""

from typing import List
import random
import pygame
import os
from game.location import Location, LocationRules


class DesertLocation(Location):

    def __init__(self, width=800, height=600):
        super().__init__(width, height)
        self.background = pygame.image.load(os.path.join("assets", "BG_images", "desert.jpg"))
        self.rules = LocationRules(
            speed_modifier=1.3,
            food_value=1,
            snake_color=(255, 255, 255),  # White color
            special_effect="dehydration"
        )
        self.generate_obstacles()
        self.water_zones = self.generate_water_zones()

    def draw(self, surface):
        """Draw desert background"""
        surface.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))

    def generate_obstacles(self) -> None:
        """Generate cacti clusters"""
        for _ in range(15):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.obstacles.append(pygame.Rect(x, y, 25, 25))

    def generate_water_zones(self) -> List[pygame.Rect]:
        """Generate life-saving oases"""
        return [pygame.Rect(100, 100, 100, 100)]  # Simplified example

    def apply_effects(self, snake) -> None:
        """Apply desert effects"""
        snake.speed *= self.rules.speed_modifier
        snake.color = self.rules.snake_color
        if self.rules.special_effect == "dehydration":
            snake.water_level = 100  # Initialize water meter