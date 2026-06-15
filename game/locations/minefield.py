from game.location import Location, LocationRules
import pygame
import random

class MinefieldLocation(Location):
    def __init__(self, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=1.0,
            food_value=1,
            snake_color=(255, 0, 0),  # Red color
            special_effect="mine_explosion"
        )
        #self.background = pygame.Surface((width, height))
        #self.background.fill((0, 0, 0))  # Black background
        self.generate_mines()
        
    def generate_mines(self):
        """Create invisible mines"""
        # Place 2 mines at specific locations
        self.obstacles = [
            pygame.Rect(self.width*0.33, self.height*0.5, self.block_size, self.block_size),
            pygame.Rect(self.width*0.66, self.height*0.5, self.block_size, self.block_size)
        ]
        
    def draw(self, screen):
        """Draw minefield background"""
        screen.fill((0, 0, 0))  # Black background
        # Optional: Draw mine positions for debugging
        #for mine in self.obstacles:
        #    pygame.draw.rect(screen, (255, 0, 0), mine, 1)

    def apply_effects(self, snake):
        """Apply minefield effects"""
        snake.speed *= self.rules.speed_modifier
        snake.color = self.rules.snake_color
        if self.rules.special_effect == "mine_explosion":
            snake.mine_effect = True