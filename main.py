import math
import pygame
from pathlib import Path
from game.snake import Snake
from game.food import Food
from game.locations import ForestLocation, DesertLocation, CityLocation, FlowerfieldLocation, HomelandLocation, CrossroadsLocation, PortalLocation
from game.highscore import HighScore
from game.particles import ParticleSystem

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        
        # Initialize particle system
        self.particle_system = ParticleSystem()
        
        # Set assets path
        self.assets_path = str(Path(__file__).parent / 'game' / 'assets')

    def _draw_menu(self, font_large, font_small, selected_option):
        """Draw the game menu."""
        # Draw menu background
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title = font_large.render("SNAKE GAME", True, (255, 255, 255))
        self.screen.blit(title, (self.screen.get_width()//2 - title.get_width()//2, 100))
        
        # Draw menu options in two columns with better spacing
        options = ["Forest", "Desert", "City", "Flowerfield", "Homeland", "Crossroads"]
        column_width = self.screen.get_width() // 2
        y_start = 200  # Starting y-position for the first item
        item_spacing = 40  # Vertical spacing between items
        
        for i, text in enumerate(options):
            color = (0, 255, 0) if i == selected_option else (255, 255, 255)
            option = font_small.render(text, True, color)
            
            # Left column (first 3 items)
            if i < len(options) // 2 + len(options) % 2:
                x = column_width // 2 - option.get_width() // 2
                y = y_start + i * item_spacing
            # Right column (remaining items)
            else:
                x = column_width + column_width // 2 - option.get_width() // 2
                y = y_start + (i - len(options) // 2 - len(options) % 2) * item_spacing
            
            self.screen.blit(option, (x, y))
        
        # Draw instructions at the bottom with smaller font
        font_tiny = pygame.font.SysFont("Arial", 20)
        instructions = font_tiny.render(
            "Use UP/DOWN to select, ENTER to start", 
            True, 
            (200, 200, 200)
        )
        self.screen.blit(instructions, (
            self.screen.get_width()//2 - instructions.get_width()//2,
            self.screen.get_height() - 50  # Fixed position near the bottom
        ))

    def run(self):
        # Music state
        current_music = None
        
        # Load menu music
        def play_menu_music():
            nonlocal current_music
            if current_music != "menu":
                try:
                    pygame.mixer.music.stop()
                    music_path = Path(__file__).parent / "game" / "assets" / "sounds" / "menu_music.mp3"
                    if music_path.exists():
                        pygame.mixer.music.load(str(music_path))
                        pygame.mixer.music.set_volume(0.3)
                        pygame.mixer.music.play(-1)
                        current_music = "menu"
                except Exception as e:
                    print(f"Menu music error: {e}")
        
        # Load location music
        def play_location_music(location_name):
            nonlocal current_music
            try:
                pygame.mixer.music.stop()
                music_path = Path(__file__).parent / "game" / "assets" / "sounds" / f"{location_name}.mp3"
                if not music_path.exists():
                    # Fallback if no specific music exists for location
                    music_path = Path(self.assets_path) / 'sounds' / 'game_music.mp3'
                if music_path.exists() and current_music != location_name:
                    pygame.mixer.music.load(str(music_path))
                    pygame.mixer.music.set_volume(0.20)  # Reset to original volume
                    pygame.mixer.music.play(-1)
                    current_music = location_name
            except Exception as e:
                print(f"Location music error: {e}")
        
        # Start with menu music
        play_menu_music()
        
        snake = Snake(width=800, height=600, block_size=14, game_engine=self)  # 30% smaller (20 * 0.7 ≈ 14)
        food = Food(width=800, height=600, assets_path=self.assets_path, block_size=27)  # 30% smaller (38 * 0.7 ≈ 27)
        high_score = HighScore()
        
        # Menu variables
        in_menu = True
        selected_option = 0
        location_names = ["forest", "desert", "city", "flowerfield", "homeland", "crossroads"]
        current_mode = location_names[selected_option]
        portal_pending = 0
        locations = [
            ForestLocation(width=800, height=600, block_size=40),
            DesertLocation(width=800, height=600, block_size=40),
            CityLocation(width=800, height=600, block_size=40),
            FlowerfieldLocation(width=800, height=600, block_size=40),
            HomelandLocation(assets_path=self.assets_path, width=800, height=600, block_size=40),
            CrossroadsLocation(width=800, height=600, block_size=40)
        ]
        
        # Fonts
        font_small = pygame.font.SysFont("Arial", 30)
        font_large = pygame.font.SysFont("Arial", 50)
        
        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if in_menu:
                        if event.key == pygame.K_UP:
                            selected_option = (selected_option - 1) % len(locations)
                        elif event.key == pygame.K_DOWN:
                            selected_option = (selected_option + 1) % len(locations)
                        elif event.key == pygame.K_RETURN:
                            in_menu = False
                            location = locations[selected_option]
                            current_mode = location_names[selected_option]
                            game_over = False
                            paused = False
                            portal_pending = 0
                            snake.current_location = location  # Set current location reference
                            snake.flower_effect = (current_mode == "flowerfield")  # Enable flower effects for flowerfield
                            # Load location-specific food images
                            food.set_location_images(f"{current_mode}_food")
                            # Play location-specific music
                            play_location_music(current_mode)
                    else:
                        if not snake.alive and event.key == pygame.K_r:
                            # Reset game
                            high_score.save_score(current_mode, snake.score)
                            snake.reset()
                            food.spawn_food()
                            if hasattr(snake, 'current_location') and hasattr(snake.current_location, 'generate_flowers'):
                                snake.current_location.generate_flowers()
                            game_over = False
                        elif event.key == pygame.K_ESCAPE:
                            # Return to menu
                            in_menu = True
                            game_over = False
                            portal_pending = 0
                            # Switch back to menu music
                            play_menu_music()
                        elif event.key == pygame.K_LEFT:
                            snake.change_direction("LEFT")
                        elif event.key == pygame.K_RIGHT:
                            snake.change_direction("RIGHT")
                        elif event.key == pygame.K_UP:
                            snake.change_direction("UP")
                        elif event.key == pygame.K_DOWN:
                            snake.change_direction("DOWN")
            
            if in_menu:
                self._draw_menu(font_large, font_small, selected_option)
            else:
                # Update particles
                self.particle_system.update()
                
                # Game logic
                if not game_over:
                    # Restore one body segment per frame while emerging from portal
                    if portal_pending > 0:
                        portal_pending -= 1
                        snake.length += 1
                        snake.score = snake.length - 1
                    
                    snake.move()
                    snake.check_collisions()
                    
                    if not snake.alive:
                        game_over = True
                        portal_pending = 0
                        high_score.save_score(current_mode, snake.score)
                    
                    if snake.eat_food(food):
                        food.spawn_food()
                    
                    # Portal check for Crossroads
                    if current_mode == "crossroads" and snake.score >= 22 and not location.portal_active:
                        location.portal_active = True
                    
                    if current_mode == "crossroads" and location.portal_active:
                        snake_head_rect = pygame.Rect(snake.x, snake.y, snake.block_size, snake.block_size)
                        if snake_head_rect.colliderect(location.portal_rect):
                            portal_pending = snake.length - 1
                            snake.body = [[snake.x, snake.y]]
                            snake.length = 1
                            snake.score = 0
                            location = PortalLocation(width=800, height=600, block_size=40)
                            current_mode = "portal"
                            snake.current_location = location
                            snake.flower_effect = False
                            play_location_music("portal")
                    
                    # Portal back from PortalLocation to Crossroads
                    if current_mode == "portal":
                        snake_head_rect = pygame.Rect(snake.x, snake.y, snake.block_size, snake.block_size)
                        if snake_head_rect.colliderect(location.portal_rect):
                            portal_pending = snake.length - 1
                            snake.body = [[snake.x, snake.y]]
                            snake.length = 1
                            snake.score = 0
                            location = CrossroadsLocation(width=800, height=600, block_size=40)
                            location.portal_active = True
                            current_mode = "crossroads"
                            snake.current_location = location
                            snake.flower_effect = False
                            snake.x = location.portal_rect.x - snake.block_size
                            snake.y = location.portal_rect.y
                            play_location_music("crossroads")
                
                # Iridescent gradient for Homeland
                if current_mode == "homeland":
                    t = pygame.time.get_ticks() / 1000
                    blend = (math.sin(t * 2) + 1) / 2
                    head_color = (
                        int(255 * blend),
                        int(255 * blend),
                        int(255 * (1 - blend))
                    )
                    tail_color = (
                        int(255 * (1 - blend)),
                        int(255 * (1 - blend)),
                        int(255 * blend)
                    )
                
                # Rendering
                location.draw(self.screen)
                food.draw(self.screen)
                if current_mode == "homeland":
                    snake.draw(self.screen, location.rules.snake_color, head_color, tail_color)
                else:
                    snake.draw(self.screen, location.rules.snake_color)
                
                # Draw particles
                self.particle_system.draw(self.screen)
                
                # UI Elements
                text_color = (0, 0, 0) if current_mode == "portal" else (255, 255, 255)
                score_text = font_small.render(f"Score: {snake.score}", True, text_color)
                high_score_text = font_small.render(
                    f"High Score: {high_score.get_high_score(current_mode)}", 
                    True, text_color
                )
                self.screen.blit(score_text, (10, 10))
                self.screen.blit(high_score_text, (10, 50))
                
                if game_over:
                    font_title = pygame.font.SysFont("Arial", 72)
                    font_instruction = pygame.font.SysFont("Arial", 42)
                    
                    # Function to create outlined text
                    def render_outlined_text(font, text, text_color, outline_color):
                        # Outline effect - render text 8 times (1px offset in each direction)
                        outline_surfaces = [
                            font.render(text, True, outline_color),
                            font.render(text, True, outline_color),
                            font.render(text, True, outline_color),
                            font.render(text, True, outline_color),
                            font.render(text, True, outline_color),
                            font.render(text, True, outline_color),
                            font.render(text, True, outline_color),
                            font.render(text, True, outline_color)
                        ]
                        text_surface = font.render(text, True, text_color)
                        
                        return outline_surfaces, text_surface
                    
                    # Create text surfaces with outline and main color
                    game_over_outlines, game_over_text = render_outlined_text(font_title, "GAME OVER", (255, 69, 0), (0, 0, 0))
                    restart_outlines, restart_text = render_outlined_text(font_instruction, "Press R to restart", (255, 255, 255), (0, 0, 0))
                    menu_outlines, menu_text = render_outlined_text(font_instruction, "Press ESC to return to menu", (200, 200, 200), (0, 0, 0))
                    
                    # Draw outlines
                    def draw_text_with_outlines(screen, outlines, text_surface, x, y):
                        center_x = x - text_surface.get_width()//2
                        center_y = y
                        
                        for i, surf in enumerate(outlines):
                            offset_x = center_x + [1, -1, 0, 0, 1, -1, 1, -1][i]
                            offset_y = center_y + [0, 0, 1, -1, 1, -1, -1, 1][i]
                            screen.blit(surf, (offset_x, offset_y))
                        screen.blit(text_surface, (center_x, center_y))
                    
                    # Center and draw all texts
                    draw_text_with_outlines(self.screen, game_over_outlines, game_over_text, 800//2, 220)
                    draw_text_with_outlines(self.screen, restart_outlines, restart_text, 800//2, 310)
                    draw_text_with_outlines(self.screen, menu_outlines, menu_text, 800//2, 370)
            
            pygame.display.update()
            self.clock.tick(10)
        
        pygame.mixer.music.stop()
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()