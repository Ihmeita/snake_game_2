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
FPS = 15
HIGHSCORE_FILE = os.path.join(os.path.expanduser("~"), "snake_highscore.txt")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
DARK_BLUE = (0, 0, 100)

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

# Fonts
font_small = pygame.font.SysFont("arial", 20)
font_medium = pygame.font.SysFont("arial", 30)
font_large = pygame.font.SysFont("arial", 50, bold=True)


def load_highscore():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0


def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        f.write(str(score))


def draw_food(x, y):
    pygame.draw.rect(screen, GREEN, [x, y, BLOCK_SIZE, BLOCK_SIZE])


def generate_food(snake=None):
    """Generate food at valid position (not on snake)"""
    if snake is None:
        snake = []

    while True:
        food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE

        if [food_x, food_y] not in snake:
            return food_x, food_y


def show_text(text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)


def game_loop():
    x, y = WIDTH // 2, HEIGHT // 2
    dx, dy = BLOCK_SIZE, 0
    snake = []
    length = 1
    food_x, food_y = generate_food()
    paused = False
    game_over = False
    highscore = load_highscore()
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif paused and event.key == pygame.K_q:
                    return "menu"

                # Movement controls (only when not paused)
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
            screen.fill(DARK_BLUE)
            show_text("PAUSED", font_large, WHITE, -30)
            show_text("Press P to continue", font_medium, WHITE, 30)
            pygame.display.update()
            clock.tick(FPS)
            continue

        if game_over:
            screen.fill(BLUE)
            show_text("GAME OVER", font_large, RED, -50)
            show_text(f"Score: {length - 1}", font_medium, WHITE, 0)
            show_text("Press SPACE to restart", font_medium, WHITE, 50)
            show_text("or Q to menu", font_small, WHITE, 90)
            pygame.display.update()
            clock.tick(FPS)
            continue

        # Move snake
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

        # Update snake body
        snake.append([x, y])
        if len(snake) > length:
            del snake[0]

        # Check self-collision
        for block in snake[:-1]:
            if block == [x, y]:
                game_over = True

        # Drawing
        screen.fill(BLUE)
        draw_food(food_x, food_y)

        # Draw snake
        for block in snake:
            pygame.draw.rect(screen, BLACK, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

        # Display score
        score_text = font_medium.render(f"Score: {length - 1}", True, WHITE)
        highscore_text = font_small.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(score_text, [10, 10])
        screen.blit(highscore_text, [10, 40])

        # Check food collision
        if x == food_x and y == food_y:
            food_x, food_y = generate_food(snake)
            length += 1

            if length - 1 > highscore:
                highscore = length - 1
                save_highscore(highscore)

        pygame.display.update()
        clock.tick(FPS)

def main_menu():
    """Main menu screen"""
    while True:
        screen.fill(BLUE)
        show_text("SNAKE GAME", font_large, WHITE, -100)

        # Display controls
        controls = [
            "ARROWS - Move",
            "P - Pause",
            "Q - Quit to menu",
            "SPACE - Restart after game over"
        ]

        for i, control in enumerate(controls):
            control_text = font_medium.render(control, True, WHITE)
            screen.blit(control_text, [WIDTH // 2 - control_text.get_width() // 2,
                                       HEIGHT // 2 + i * 40])

        # Start prompt
        start_text = font_medium.render("Press SPACE to start", True, GREEN)
        screen.blit(start_text, [WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 100])

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return "start"
                elif event.key == pygame.K_q:
                    return "quit"


# Main game flow
def run_game():
    """Manages game states"""
    while True:
        # Start with menu
        menu_action = main_menu()
        if menu_action == "quit":
            break

        # Start game
        game_result = game_loop()

        # Handle game over
        while game_result == "restart":
            game_result = game_loop()

        if game_result == "quit":
            break
    pygame.quit()


if __name__ == "__main__":
    run_game()