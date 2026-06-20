from game.location import Location, LocationRules
import pygame
import random
import os

class FlowerfieldLocation(Location):
    def __init__(self, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=1.0,
            food_value=1,
            snake_color=(255, 0, 0),  # Red color
            special_effect="flower_explosion"
        )
        sound_path = os.path.join(os.path.dirname(__file__), "../../assets/sounds/flowerfield.mp3")
        self.flower_sound = pygame.mixer.Sound(sound_path)
        bg_path = os.path.join(os.path.dirname(__file__), "../assets/BG_images/flowerfield.jpg")
        try:
            self.background = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(self.background, (width, height))
        except Exception as e:
            print(f"Error loading background: {e}")
            self.background = pygame.Surface((width, height))
            self.background.fill((0, 0, 0))  # Fallback black background
        self.generate_flowers()
        
    def generate_flowers(self):
        """Create flower bushes at random positions"""
        self.obstacles = []
        for _ in range(2):  # Creates 2 flower bushes
            flower_x = random.randint(1, (self.width // self.block_size) - 2) * self.block_size
            flower_y = random.randint(1, (self.height // self.block_size) - 2) * self.block_size
            self.obstacles.append(pygame.Rect(flower_x, flower_y, self.block_size, self.block_size))
        
    def draw(self, screen):
        """Draw flowerfield background"""
        screen.blit(self.background, (0, 0))
        # Optional: Draw flower positions for debugging
        #for flower in self.obstacles:
        #    pygame.draw.rect(screen, (255, 0, 0), flower, 1)

    def apply_effects(self, snake):
        """Apply flowerfield effects"""
        snake.speed *= self.rules.speed_modifier
        snake.color = self.rules.snake_color
        if self.rules.special_effect == "flower_explosion":
            snake.flower_effect = True
            self.flower_sound.play()