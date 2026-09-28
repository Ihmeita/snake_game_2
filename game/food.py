import pygame
import random
from typing import Tuple
from pathlib import Path

class Food:
    def __init__(self, width: int = 800, height: int = 600, block_size: int = 38, assets_path: str = None):
        self.width = width
        self.height = height
        self.block_size = block_size
        self.x = 0
        self.y = 0
        self.is_special = False
        self.spawn_time = 0
        self._assets_path = assets_path
        
        # Load images
        self._load_images(assets_path)
        self.spawn_food()
        
    def _load_images(self, assets_path, prefix="food"):
        """Load food images with visual scaling"""
        try:
            if assets_path:
                normal_path = Path(__file__).parent / "assets" / "images" / f"{prefix}.png"
                special_path = Path(__file__).parent / "assets" / "images" / f"{prefix}_special.png"
                
                if not normal_path.exists():
                    normal_path = Path(__file__).parent / "assets" / "images" / "food.png"
                if not special_path.exists():
                    special_path = Path(__file__).parent / "assets" / "images" / "special_food.png"
                
                self.normal_img = pygame.image.load(str(normal_path))
                self.special_img = pygame.image.load(str(special_path))
                
                # Scale images to 93% of block_size (visual only)
                visual_size = int(self.block_size * 0.93)
                self.normal_img = pygame.transform.scale(self.normal_img, (visual_size, visual_size))
                self.special_img = pygame.transform.scale(self.special_img, (visual_size, visual_size))
            else:
                raise FileNotFoundError("No assets path provided")
        except Exception:
            # Fallback to pixel style
            self.normal_img = None
            self.special_img = None
    
    def set_location_images(self, prefix):
        """Reload food images for a specific location (e.g. 'homeland_food')"""
        self._load_images(getattr(self, '_assets_path', None), prefix)

    def spawn_food(self):
        """Spawn food at random position with 20% chance for special food"""
        self.x = round(random.randrange(0, self.width - self.block_size) / self.block_size) * self.block_size
        self.y = round(random.randrange(0, self.height - self.block_size) / self.block_size) * self.block_size

        self.is_special = random.random() < 0.15
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, screen: pygame.Surface, visible=True):
        """Draw food on screen"""
        if not visible:
            return
        if self.normal_img and self.special_img:
            img = self.special_img if self.is_special else self.normal_img
            # Calculate centered position for scaled image
            visual_size = img.get_width()
            offset = (self.block_size - visual_size) // 2
            screen.blit(img, (self.x + offset, self.y + offset))
        else:
            # Fallback to pixel style (7% smaller)
            visual_size = int(self.block_size * 0.93)
            offset = (self.block_size - visual_size) // 2
            
            color = (255, 192, 203) if self.is_special else (0, 255, 0)
            pygame.draw.rect(
                screen, 
                color,
                [self.x + offset, self.y + offset, visual_size, visual_size]
            )
            
            # Add white outline (7% smaller)
            pygame.draw.rect(
                screen, 
                (255, 255, 255),  
                [self.x + offset, self.y + offset, visual_size, visual_size],
                2  # Outline width
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