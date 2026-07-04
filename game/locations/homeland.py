from game.location import Location, LocationRules  # Absolute import
import pygame
import random
import os

class HomelandLocation(Location):
    def __init__(self, assets_path, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=0.4,
            food_value=2,
            snake_color=(0, 0, 0)  # Black color
        )
        self.background = pygame.image.load(
            os.path.join(assets_path, "BG_images", "homeland.jpg")
            )
        self.explosion_particles = []
        self.obstacles = []
        self.initial_obstacles = []

        self.generate_obstacles()
        
    def full_reset(self):
        """Completely reset all obstacles and state"""
        self.obstacles = []
        self.initial_obstacles = []
        self.explosion_particles = []
        self.generate_obstacles()
        self.ghost_timer = 60

    def generate_obstacles(self):
        """Create obstacles with safe spawn zone and initial visibility"""
        # Clear existing obstacles
        self.obstacles = []
        
        # Safe zone where snake spawns (no obstacles)
        safe_zone = pygame.Rect(100, 100, 200, 200)
        
        # Generate 10 obstacles
        for _ in range(10):
            while True:
                x = random.randint(50, self.width-50)
                y = random.randint(50, self.height-50)
                obstacle = pygame.Rect(x, y, 30, 30)
                if not obstacle.colliderect(safe_zone):
                    self.obstacles.append(obstacle)
                    break
        
        # Store initial obstacles for ghost effect
        self.initial_obstacles = self.obstacles.copy()
        self.ghost_timer = 60  # ~2 seconds at 30 FPS
        
    def reset(self):
        """Reset location state including regenerating ALL obstacles"""
        self.obstacles = []  # Clear existing obstacles
        self.initial_obstacles = []  # Clear ghost obstacles
        self.generate_obstacles()  # Generate fresh obstacles
        self.explosion_particles = []  # Clear any particles
        self.ghost_timer = 60  # Reset ghost timer

    def check_collisions(self, snake):
        """Check for obstacle collisions and handle explosions"""
        head_rect = pygame.Rect(snake.x, snake.y, snake.block_size, snake.block_size)
        for obstacle in self.obstacles[:]:
            if head_rect.colliderect(obstacle):
                self.create_explosion(obstacle.x + 15, obstacle.y + 15)
                self.obstacles.remove(obstacle)
                snake.score = max(0, snake.score - 2)
                # Game over if score reaches 0
                if snake.score <= 0:
                    snake.alive = False
                return False

    def create_explosion(self, x, y):
        """Create explosion particles"""
        for _ in range(20):
            angle = random.uniform(0, 2 * 3.1416)
            speed = random.uniform(1, 5)
            self.explosion_particles.append({
                'x': x,
                'y': y,
                'dx': speed * pygame.math.Vector2(1, 0).rotate(angle * 180/3.1416).x,
                'dy': speed * pygame.math.Vector2(1, 0).rotate(angle * 180/3.1416).y,
                'size': random.randint(3, 8),
                'life': random.randint(20, 40)
            })

    def update_explosions(self):
        """Update explosion particles"""
        for particle in self.explosion_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.explosion_particles.remove(particle)

    def apply_effects(self, snake):
        """Apply effects to snake"""
        snake.speed *= self.rules.speed_modifier
        snake.color = self.rules.snake_color

    def draw(self, screen):
        """Draw location background, invisible obstacles (with collision) and explosions"""
        screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))
        
        # Draw ghost obstacles if timer is active (briefly visible at start)
        if hasattr(self, 'ghost_timer') and self.ghost_timer > 0:
            for obstacle in self.initial_obstacles:
                ghost_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
                ghost_surface.fill((255, 255, 255, 128))  # Semi-transparent white
                screen.blit(ghost_surface, (obstacle.x, obstacle.y))
            self.ghost_timer -= 1
        
        # Draw explosions (only visible effect when hitting invisible obstacles)
        for particle in self.explosion_particles:
            pygame.draw.circle(screen, (255, 165, 0), (int(particle['x']), int(particle['y'])), particle['size'])
            
    def check_collisions(self, snake):
        """Check for obstacle collisions (works even when obstacles are invisible)"""
        head_rect = pygame.Rect(snake.x, snake.y, snake.block_size, snake.block_size)
        for obstacle in self.obstacles[:]:
            if head_rect.colliderect(obstacle):
                self.create_explosion(obstacle.x + 15, obstacle.y + 15)
                self.obstacles.remove(obstacle)
                snake.score = max(0, snake.score - 2)
                if snake.score <= 0:
                    snake.alive = False
                return False