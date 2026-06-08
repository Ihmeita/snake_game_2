import json
from pathlib import Path

class HighScore:
    def __init__(self):
        self.file_path = Path('highscores.json')
        self.scores = self._load_scores()
    
    def _load_scores(self):
        try:
            if self.file_path.exists():
                with open(self.file_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"normal": 0, "forest": 0, "desert": 0}
    
    def save_score(self, mode: str, score: int):
        if score > self.scores.get(mode, 0):
            self.scores[mode] = score
            try:
                with open(self.file_path, 'w') as f:
                    json.dump(self.scores, f, indent=4)
            except Exception:
                pass
    
    def get_high_score(self, mode: str) -> int:
        return self.scores.get(mode, 0)