"""
Game Engine Module - Fixed Implementation
"""

from typing import Type, Optional, Dict, Any
import pygame
from pathlib import Path
from game.location import Location
from game.snake import Snake

class GameEngine:
    """Main game engine class."""

    def __init__(self, screen_width: int = 800, screen_height: int = 600, fps: int = 60):
        """Initialize game with specified settings."""
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = False

        self.current_location: Optional[Location] = None
        self.snake: Optional[Snake] = None
        self.assets: Dict[str, Any] = {'sounds': {}, 'images': {}}

        self._load_assets()

    def _load_assets(self) -> None:
        """Load game assets with error handling."""
        try:
            assets_path = Path(__file__).parent / 'assets'
            
            # Create assets directory if it doesn't exist
            assets_path.mkdir(exist_ok=True)
            (assets_path / 'images').mkdir(exist_ok=True)
            (assets_path / 'sounds').mkdir(exist_ok=True)

            # Load sounds
            sound_files = {
                'eat': 'eat.wav',
                'death': 'death.wav',
                'music': 'game_music.mp3'
            }

            for name, filename in sound_files.items():
                full_path = assets_path / 'sounds' / filename
                if full_path.exists():
                    self.assets['sounds'][name] = pygame.mixer.Sound(full_path)
                    
            # Load images (add any existing images to assets dict)
            self.assets_path = str(assets_path)
            
        except Exception as e:
            print(f"Error loading assets: {e}")

    def set_location(self, location_class: Type[Location]) -> None:
        """Set the current game location."""
        self.current_location = location_class(
            width=self.screen.get_width(),
            height=self.screen.get_height()
        )

        if not self.snake:
            self.snake = Snake()
        self.current_location.apply_effects(self.snake)

    def run(self) -> None:
        """Run the main game loop."""
        if not self.current_location:
            raise ValueError("No location set! Call set_location() first")

        self.running = True
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(self.fps)

        pygame.quit()

    def _handle_events(self) -> None:
        """Process all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        """Handle keyboard input."""
        if not self.snake:
            return

        if event.key == pygame.K_LEFT:
            self.snake.change_direction('LEFT')
        elif event.key == pygame.K_RIGHT:
            self.snake.change_direction('RIGHT')
        elif event.key == pygame.K_UP:
            self.snake.change_direction('UP')
        elif event.key == pygame.K_DOWN:
            self.snake.change_direction('DOWN')

    def _update(self) -> None:
        """Update game state."""
        if not self.snake:
            return

        self.snake.move()

        # Add your collision detection here
        # Example:
        # if self.check_collision():
        #     self.game_over()

    def _render(self) -> None:
        """Render game frame."""
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Draw location
        if self.current_location:
            self.current_location.draw(self.screen)

        # Draw snake
        if self.snake and self.current_location:
            self.snake.draw(self.screen, self.current_location.rules.snake_color)

        pygame.display.flip()