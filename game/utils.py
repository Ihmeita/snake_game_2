import os
import pygame
from pathlib import Path

class Config:
    # Core game settings
    WIDTH, HEIGHT = 800, 600
    BLOCK_SIZE = 20
    FPS = 10
    
    # Path configurations
    ASSETS_PATH = Path(__file__).parent.parent / "assets"
    HIGHSCORE_FILE = os.path.join(os.path.expanduser("~"), "snake_highscore.txt")
    
    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (213, 50, 80)
    GREEN = (0, 255, 0)
    
    @classmethod
    def init_assets(cls):
        """Ensure assets directory exists"""
        cls.ASSETS_PATH.mkdir(exist_ok=True)
        
        # Sound file paths
        cls.EAT_SOUND = cls.ASSETS_PATH / "eat.wav"
        cls.DEATH_SOUND = cls.ASSETS_PATH / "death.wav"
        cls.MENU_MUSIC = cls.ASSETS_PATH / "menu_music.mp3"
        cls.GAME_MUSIC = cls.ASSETS_PATH / "game_music.mp3"