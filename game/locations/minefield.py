from game.location import Location, LocationRules
import pygame
import random
import os

class MinefieldLocation(Location):
    def __init__(self, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=1.0,
            food_value=1,
            snake_color=(255, 0, 0),  # Red color
            special_effect="mine_explosion"
        )
        sound_path = os.path.join(os.path.dirname(__file__), "../../assets/sounds/minefield.mp3")
        self.mine_sound = pygame.mixer.Sound(sound_path)
        #self.background = pygame.Surface((width, height))
        #self.background.fill((0, 0, 0))  # Black background
        self.generate_mines()
        
    def generate_mines(self):
        """Create invisible mines at random positions"""
        # Clear existing mines
        self.obstacles = []
        
        # Generate random positions for mines
        for _ in range(2):  # Creates 2 mines
            mine_x = random.randint(1, (self.width // self.block_size) - 2) * self.block_size
            mine_y = random.randint(1, (self.height // self.block_size) - 2) * self.block_size
            self.obstacles.append(pygame.Rect(mine_x, mine_y, self.block_size, self.block_size))
        
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
            self.mine_sound.play()