from game.location import Location, LocationRules  # Absolute import
import pygame
import random
import os

class Location1(Location):
    def __init__(self, assets_path, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=0.4,
            food_value=2,
            snake_color=(128, 0, 128)  # Purple color
        )
        self.background = pygame.image.load(os.path.join(assets_path, "BG_images", "1.jpg"))
        self.generate_obstacles()

    def generate_obstacles(self):
        """Create obstacles"""
        for _ in range(15):
            x = random.randint(50, self.width-50)
            y = random.randint(50, self.height-50)
            self.obstacles.append(pygame.Rect(x, y, 30, 30))

    def apply_effects(self, snake):
        """Apply effects to snake"""
        snake.speed *= self.rules.speed_modifier
        snake.color = self.rules.snake_color

    def draw(self, screen):
        """Draw location background"""
        screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))