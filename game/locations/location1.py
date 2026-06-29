from game.location import Location, LocationRules  # Absolute import
import pygame
import random
import os

class Location1(Location):
    def __init__(self, assets_path, width=800, height=600, block_size=40):
        super().__init__(width, height, block_size)
        self.rules = LocationRules(
            speed_modifier=0.4,
            food_value=2,
            snake_color=(128, 0, 128)  # Purple color
        )
        self.background = pygame.image.load(os.path.join(assets_path, "BG_images", "1.jpg"))
        self.explosion_particles = []
        self.generate_obstacles()

    def generate_obstacles(self):
        """Create obstacles"""
        for _ in range(15):
            x = random.randint(50, self.width-50)
            y = random.randint(50, self.height-50)
            self.obstacles.append(pygame.Rect(x, y, 30, 30))

    def check_collisions(self, snake):
        """Check for obstacle collisions and handle explosions"""
        head_rect = pygame.Rect(snake.x, snake.y, snake.block_size, snake.block_size)
        for obstacle in self.obstacles[:]:
            if head_rect.colliderect(obstacle):
                self.create_explosion(obstacle.x + 15, obstacle.y + 15)
                self.obstacles.remove(obstacle)
                snake.score = max(0, snake.score - 2)
                return snake.score <= 0
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
        """Draw location background, obstacles and explosions"""
        screen.blit(pygame.transform.scale(self.background, (self.width, self.height)), (0, 0))
        for obstacle in self.obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle)  # Changed to bright red for better visibility
            pygame.draw.rect(screen, (255, 255, 255), obstacle, 1)  # White border for contrast
        for particle in self.explosion_particles:
            pygame.draw.circle(screen, (255, 165, 0), (int(particle['x']), int(particle['y'])), particle['size'])