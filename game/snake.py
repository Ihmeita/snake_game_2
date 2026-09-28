import pygame
from pathlib import Path
from typing import Tuple, List
import random

class Snake:
    def __init__(self, width: int = 800, height: int = 600, block_size: int = 20, game_engine=None):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.game_engine = game_engine  # Store reference to game engine
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
        self.flower_effect = hasattr(self, 'current_location') and hasattr(self.current_location, 'rules') and hasattr(self.current_location.rules, 'special_effect') and "flower" in str(self.current_location.rules.special_effect).lower()

    def _load_sounds(self):
        """Load sound effects"""
        sound_dir = Path(__file__).parent / "assets" / "sounds"
        
        # Initialize with None (will be safe to call play() on None)
        self.eat_sound = None
        self.death_sound = None
        self.flower_sound = None
        
        try:
            eat_path = sound_dir / "eat.wav"
            if eat_path.exists():
                self.eat_sound = pygame.mixer.Sound(str(eat_path))
                self.eat_sound.set_volume(0.65)
            
            death_path = sound_dir / "death.wav"
            if death_path.exists():
                self.death_sound = pygame.mixer.Sound(str(death_path))
                self.death_sound.set_volume(0.65)
                
            flower_path = sound_dir / "flowerbush.wav"
            if flower_path.exists():
                self.flower_sound = pygame.mixer.Sound(str(flower_path))
                self.flower_sound.set_volume(0.65)
        except Exception as e:
            print(f"Could not load sounds: {e}")

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
        """Check for self-collisions and obstacle collisions"""
        head_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
        
        # Self collision
        head_pos = [self.x, self.y]
        if head_pos in self.body[:-1]:
            self.alive = False
            if self.death_sound:
                self.death_sound.play()
                
        # Check for obstacle collisions (only if current_location has obstacles)
        if hasattr(self, 'current_location') and hasattr(self.current_location, 'check_collisions'):
            if self.current_location.check_collisions(self):
                self.alive = False
                if self.death_sound:
                    self.death_sound.play()
                    
    def create_particles(self):
        """Create explosion particles when hitting a flower bush"""
        # This would be implemented in the game loop to animate particles
        # Placeholder implementation
        print("BOOM! Particle explosion!")

    def eat_food(self, food):
        """Handle food consumption with collision detection"""
        # Use food's logical size (38px) for collision detection
        snake_rect = pygame.Rect(self.x, self.y, self.block_size, self.block_size)
        food_rect = pygame.Rect(food.x, food.y, food.block_size, food.block_size)
        
        if snake_rect.colliderect(food_rect):
            if food.is_special:
                self.score += 3  # Bonus points only
                self.length += 1  # Normal growth
                self.outline_color = (255, 192, 203)
            else:
                self.score += 1
                self.length += 1
                self.outline_color = (0, 255, 0)
            if self.eat_sound:
                self.eat_sound.play()
            return True
        return False

    def draw(self, screen, snake_color, gradient_from=None, gradient_to=None, visible=True):
        """Draw snake on screen"""
        if not visible:
            return
        total = len(self.body)
        for i, segment in enumerate(self.body):
            if gradient_from and gradient_to:
                t = i / max(total - 1, 1)
                outline = (
                    int(gradient_from[0] + (gradient_to[0] - gradient_from[0]) * t),
                    int(gradient_from[1] + (gradient_to[1] - gradient_from[1]) * t),
                    int(gradient_from[2] + (gradient_to[2] - gradient_from[2]) * t)
                )
            else:
                outline = (255, 255, 255)
            
            pygame.draw.rect(
                screen, 
                outline,
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