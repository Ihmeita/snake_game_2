from game.location import Location, LocationRules
import pygame
import os

class CityLocation(Location):
    def __init__(self, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.background = pygame.image.load(os.path.join("assets", "BG_images", "city.jpg"))
        self.rules = LocationRules(
            speed_modifier=1.0,
            food_value=1,
            snake_color=(0, 100, 0)  # Dark green color
        )
        self.generate_buildings()
        
    def generate_buildings(self):
        """Create building obstacles"""
        # Create sample buildings (3 vertical rectangles)
        building_width = 80
        spacing = self.width // 4
        
        self.obstacles = [
            pygame.Rect(spacing, 300, building_width, 250),
            pygame.Rect(spacing*2, 200, building_width, 350),
            pygame.Rect(spacing*3, 250, building_width, 300)
        ]
        
    def draw(self, screen):
        """Draw city background"""
        screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))