🐍 Snake Game


**Classic Snake game** with modern features: persistent highscore, intuitive controls.

Features
- 🏆 **Persistent Highscore** - Saves your best score between sessions
- 🕹️ **Responsive controls** - Keyboard (arrows) + Mouse support
- 🔄 **Infinite gameplay** - Snake wraps around screen edges
- 🎨 **Clean UI** - Animated buttons and score display

Quick Start

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   
2. Run the game:
python s_main.py

4. Controls:
- SPACE - Start game  
- ESC - Quit  
- Arrow keys - Move snake  
- SPACE - Restart after Game Over  
- Q - Return to menu
- P - Pause game


Project Structure
snake/

├── s_main.py

├── requirements.txt

├── .gitignore

├── background.jpg

Customization
- Change colors: Edit the RGB values at the top of s_main.py
- Adjust speed: Modify snake_speed variable
- Highscore location: Change highscore_path if needed

Notes
- Highscores are saved to:  
C:\Users\[YourUsername]\snake_highscore.txt (Windows)  
 or current directory if alternate path is set
