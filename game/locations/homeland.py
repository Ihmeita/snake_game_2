from game.location import Location, LocationRules
import pygame
import os

class HomelandLocation(Location):
    def __init__(self, assets_path, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=0.4,
            food_value=2,
            snake_color=(0, 0, 0)  # Black color
        )
        self.background = pygame.image.load(
            os.path.join(assets_path, "BG_images", "homeland.jpg")
            )
        self.obstacles = []

    def apply_effects(self, snake):
        """Apply effects to snake"""
        snake.speed *= self.rules.speed_modifier
        snake.color = self.rules.snake_color

    def draw(self, screen):
        """Draw location background"""
        screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))