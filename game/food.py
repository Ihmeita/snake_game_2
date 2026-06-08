import pygame
import random
from typing import Tuple

class Food:
    def __init__(self, width: int = 800, height: int = 600, block_size: int = 20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.x = 0
        self.y = 0
        self.is_special = False
        self.spawn_time = 0
        self.color = (0, 255, 0)       # Green for normal food
        self.special_color = (255, 192, 203)  # Pink for special food
        self.spawn_food()

    def spawn_food(self):
        """Spawn food at random position"""
        self.x = round(random.randrange(0, self.width - self.block_size) / self.block_size) * self.block_size
        self.y = round(random.randrange(0, self.height - self.block_size) / self.block_size) * self.block_size
        
        # 10% chance for special food
        self.is_special = random.random() < 0.1
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface):
        """Draw food on screen"""
        color = self.special_color if self.is_special else self.color
        pygame.draw.rect(
            screen, 
            color,
            [self.x, self.y, self.block_size, self.block_size]
        )
        
        # Add white outline to all apples
        pygame.draw.rect(
            screen, 
            (255, 255, 255),  
            [self.x, self.y, self.block_size, self.block_size],
            2  # Outline width
        )
        
        # Draw sparkle effect for special food
        if self.is_special:
            pygame.draw.circle(screen, (255, 255, 255), 
                              (self.x + self.block_size//2, self.y + self.block_size//2), 
                              self.block_size//3, 2)