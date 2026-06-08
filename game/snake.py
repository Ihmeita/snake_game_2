import pygame
from pathlib import Path
from typing import Tuple, List
import random

class Snake:
    def __init__(self, width: int = 800, height: int = 600, block_size: int = 20):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.reset()
        self._load_sounds()

    def reset(self):
        """Reset snake to initial state"""
        self.x = self.width // 2
        self.y = self.height // 2
        self.dx = self.block_size
        self.dy = 0
        self.next_direction = "RIGHT"
        self.body = [[self.x, self.y]]
        self.length = 1
        self.score = 0
        self.outline_color = (0, 255, 0)
        self.alive = True

    def _load_sounds(self):
        """Load sound effects"""
        try:
            self.eat_sound = pygame.mixer.Sound("assets/sounds/eat.wav")
            self.death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
            self.eat_sound.set_volume(0.65)  # Set to 65% volume
            self.death_sound.set_volume(0.65)  # Set to 65% volume
        except Exception as e:
            print(f"Could not load sounds: {e}")
            # Create silent sounds as fallback
            silent_wav = bytearray([82,73,70,70,24,0,0,0,87,65,86,69,102,109,116,32,16,0,0,0,1,0,1,0,68,172,0,0,136,88,1,0,2,0,16,0,100,97,116,97,0,0,0,0])
            self.eat_sound = pygame.mixer.Sound(buffer=silent_wav)
            self.death_sound = pygame.mixer.Sound(buffer=silent_wav)
            self.eat_sound.set_volume(0.65)
            self.death_sound.set_volume(0.65)

    def move(self):
        """Update snake position"""
        if not self.alive:
            return
            
        # Update direction
        if self.next_direction == "LEFT" and self.dx == 0:
            self.dx, self.dy = -self.block_size, 0
        elif self.next_direction == "RIGHT" and self.dx == 0:
            self.dx, self.dy = self.block_size, 0
        elif self.next_direction == "UP" and self.dy == 0:
            self.dx, self.dy = 0, -self.block_size
        elif self.next_direction == "DOWN" and self.dy == 0:
            self.dx, self.dy = 0, self.block_size

        # Move head
        self.x += self.dx
        self.y += self.dy

        # Screen wrapping
        self.x = self.x % self.width
        self.y = self.y % self.height

        # Update body
        self.body.append([self.x, self.y])
        if len(self.body) > self.length:
            self.body.pop(0)

    def change_direction(self, direction: str):
        """Change movement direction"""
        opposites = {"LEFT":"RIGHT", "RIGHT":"LEFT", "UP":"DOWN", "DOWN":"UP"}
        if direction != opposites.get(self.next_direction):
            self.next_direction = direction

    def check_collisions(self):
        """Check for self-collisions"""
        head = [self.x, self.y]
        if head in self.body[:-1]:
            self.alive = False
            if self.death_sound:
                self.death_sound.play()

    def eat_food(self, food):
        """Handle food consumption"""
        if self.x == food.x and self.y == food.y:
            if food.is_special:
                self.length += 3
                self.outline_color = (255, 192, 203)  # Pink outline (matches special food)
            else:
                self.length += 1
                self.outline_color = (0, 255, 0)  # Green outline (matches normal food)
            
            self.score = self.length - 1
            if self.eat_sound:
                self.eat_sound.play()
            return True
        return False

    def draw(self, screen, snake_color):
        """Draw snake on screen"""
        for segment in self.body:
            pygame.draw.rect(
                screen, 
                self.outline_color,
                [segment[0]-1, segment[1]-1, self.block_size+2, self.block_size+2],
                1
            )
            pygame.draw.rect(
                screen, 
                snake_color,
                [segment[0], segment[1], self.block_size, self.block_size]
            )
        
        # Draw score
        font = pygame.font.SysFont("Arial", 30)
        score_text = font.render(f"Score: {self.score}", True, (255,255,255))
        screen.blit(score_text, (10, 10))