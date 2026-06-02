import pygame
import random
import os

# Initialize pygame
pygame.init()

# Global clock
clock = pygame.time.Clock()

# Game settings
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
FPS = 10
HIGHSCORE_FILE = os.path.join(os.path.expanduser("~"), "snake_highscore.txt")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
DARK_BLUE = (0, 0, 100)
RED_APPLE = (255, 0, 0)  # Special red apple color
SPECIAL_APPLE_CHANCE = 0.2  # 20% chance to spawn special apple

# Sound effects
eat_sound = None
death_sound = None
try:
    eat_sound = pygame.mixer.Sound("sounds/eat.wav")
    death_sound = pygame.mixer.Sound("sounds/death.wav")
except:
    print("Could not load sound effects")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# NEW: Improved bold fonts with outlines
font_small = pygame.font.SysFont("Arial Black", 20)
font_medium = pygame.font.SysFont("Arial Black", 30, bold=True)
font_large = pygame.font.SysFont("Arial Black", 50, bold=True)

# NEW: Background loading
background = None
try:
    bg_path = os.path.join(os.path.dirname(__file__), "background.jpg")
    if os.path.exists(bg_path):
        background = pygame.image.load(bg_path).convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
except:
    background = None


# NEW: Enhanced text rendering with outline
def show_text(text, font, color, y_offset=0, outline_color=None):
    """Render text with optional outline"""
    if outline_color:
        # Render outline by slightly offsetting the text
        offsets = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        for dx, dy in offsets:
            text_outline = font.render(text, True, outline_color)
            text_rect = text_outline.get_rect(center=(WIDTH // 2 + dx, HEIGHT // 2 + y_offset + dy))
            screen.blit(text_outline, text_rect)

    # Main text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)


def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0


def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))


# NEW: Improved food drawing with white outline
def draw_food(x, y, is_special):
    """Draw food with white outline"""
    color = RED_APPLE if is_special else GREEN
    # White outline
    pygame.draw.rect(screen, WHITE, [x - 1, y - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2], 1)
    # Main food color
    pygame.draw.rect(screen, color, [x, y, BLOCK_SIZE, BLOCK_SIZE])


def generate_food(snake=None):
    """Generate food at valid position (not on snake)"""
    if snake is None:
        snake = []

    while True:
        food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

        if [food_x, food_y] not in snake:
            is_special = random.random() < SPECIAL_APPLE_CHANCE
            return food_x, food_y, is_special


def game_loop():
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = BLOCK_SIZE, 0
    snake = []
    length = 1
    food_x, food_y, is_special = generate_food()
    paused = False
    game_over = False
    highscore = load_highscore()
    snake_outline = GREEN  # NEW: Initialize snake outline color

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif paused and event.key == pygame.K_q:
                    return "menu"

                if not paused and not game_over:
                    if event.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -BLOCK_SIZE, 0
                    elif event.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = BLOCK_SIZE, 0
                    elif event.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -BLOCK_SIZE
                    elif event.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, BLOCK_SIZE
                elif game_over and event.key == pygame.K_SPACE:
                    return "restart"
                elif game_over and event.key == pygame.K_q:
                    return "menu"

        if paused:
            if background:
                screen.blit(background, (0, 0))
            else:
                screen.fill(DARK_BLUE)
            show_text("PAUSED", font_large, WHITE, -30, BLACK)  # NEW: With outline
            show_text("Press P to continue", font_medium, WHITE, 30, BLACK)
            pygame.display.update()
            clock.tick(FPS)
            continue

        if game_over:
            if background:
                screen.blit(background, (0, 0))
            else:
                screen.fill(BLUE)
            show_text("GAME OVER", font_large, RED, -50, BLACK)  # NEW: With outline
            show_text(f"Score: {length - 1}", font_medium, WHITE, 0, BLACK)
            show_text("Press SPACE to restart", font_medium, WHITE, 50, BLACK)
            show_text("or Q to menu", font_small, WHITE, 90, BLACK)
            pygame.display.update()
            clock.tick(FPS)
            continue

        # Game logic
        x += dx
        y += dy

        # Screen wrapping
        if x >= WIDTH:
            x = 0
        elif x < 0:
            x = WIDTH - BLOCK_SIZE
        if y >= HEIGHT:
            y = 0
        elif y < 0:
            y = HEIGHT - BLOCK_SIZE

        snake.append([x, y])
        if len(snake) > length:
            del snake[0]

        # Collision check
        for block in snake[:-1]:
            if block == [x, y]:
                if death_sound:
                    death_sound.play()
                game_over = True

        # Drawing
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLUE)

        # Draw food
        draw_food(food_x, food_y, is_special)

        # NEW: Enhanced snake drawing with dynamic outline
        for block in snake:
            pygame.draw.rect(screen, snake_outline, [block[0] - 1, block[1] - 1, BLOCK_SIZE + 2, BLOCK_SIZE + 2], 1)
            pygame.draw.rect(screen, BLACK, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

        # Display score
        score_text = font_medium.render(f"Score: {length - 1}", True, WHITE)
        highscore_text = font_small.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(score_text, [10, 10])
        screen.blit(highscore_text, [10, 40])

        # Check food collision
        if x == food_x and y == food_y:
            if eat_sound:
                eat_sound.play()
            length += 3 if is_special else 1
            snake_outline = RED_APPLE if is_special else GREEN  # NEW: Change outline color
            food_x, food_y, is_special = generate_food(snake)

            if is_special:
                special_text = font_small.render("SPECIAL APPLE!", True, WHITE)
                screen.blit(special_text, [10, 70])

            if length - 1 > highscore:
                highscore = length - 1
                save_highscore(highscore)

        pygame.display.update()
        clock.tick(FPS)


def main_menu():
    """Main menu screen"""
    # Initialize music
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("sounds/menu_music.mp3")
        pygame.mixer.music.set_volume(0.5)  # Set volume to 50%
        pygame.mixer.music.play(-1)  # Loop indefinitely
    except:
        print("Could not load music file")

    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLUE)

        # NEW: Improved menu text with outlines
        show_text("SNAKE GAME", font_large, WHITE, -100, BLACK)

        controls = [
            "ARROWS - Move",
            "P - Pause",
            "Q - Quit to menu",
            "SPACE - Restart after game over"
        ]

        for i, control in enumerate(controls):
            show_text(control, font_medium, WHITE, -50 + i * 40, BLACK)

        show_text("Press SPACE to start", font_medium, GREEN, 140, BLACK)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.fadeout(500)  # Fade out over 0.5s
                    return "start"
                elif event.key == pygame.K_q:
                    pygame.mixer.music.stop()
                    return "quit"


def run_game():
    """Manages game states"""
    while True:
        menu_action = main_menu()
        if menu_action == "quit":
            break

        game_result = game_loop()
        while game_result == "restart":
            game_result = game_loop()

        if game_result == "quit":
            break
    pygame.quit()


if __name__ == "__main__":
    run_game()