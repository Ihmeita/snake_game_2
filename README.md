A modern Python implementation of the classic Snake game (created with assistance from OpenCode AI) with:
- Multiple gameplay locations (Forest, Desert, City)
- Menu system with background music
- Location-specific music and visuals
- High score tracking
- Sound effects for eating and game over

## Features
- **Three Unique Locations**: Each with its own theme, background image, and original soundtrack created by [Imro69](https://soundcloud.com/imro69)
- **Audio System**: Background music and sound effects
- **Menu Navigation**: Choose locations with keyboard (UP/DOWN arrows)
- **High Scores**: Saved and displayed for each location
- **Game Controls**: Arrow keys to move, ESC to return to menu, R to restart
-  (Note: Desert location will eventually be renamed to Galaxy)

## Installation
1. Clone this repository:
   ```
   git clone https://github.com/Ihmeita/snake_game_2.git
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Requirements
- Python 3.7+
- Pygame

## How to Play
1. Run `main.py`
2. Use UP/DOWN arrows to select location (Forest, Desert, City)
3. Press ENTER to start
4. Use arrow keys to control the snake
5. Eat food to grow longer and increase score
6. Avoid walls and your own tail
7. Press R to restart or ESC to return to menu

## File Structure
```
assets/
    BG_images/     # Background images for each location
    sounds/        # Music and sound effects
game/             # Core game logic
    locations/     # Location-specific implementations
    engine.py      # Game engine basics
    food.py        # Food mechanics
    game_states.py # Game states management
    highscore.py   # High score tracking
    menu.py        # Menu system
    snake.py       # Snake mechanics
    utils.py       # Helper functions
main.py           # Main game loop
requirements.txt  # Dependency list
```

## Contributing
Contributions are welcome! Please open an issue or pull request for any bugs or feature requests.
