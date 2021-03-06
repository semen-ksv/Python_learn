with open('high_score.txt', 'r') as fp:
    line = fp.readline()
    hi_score = int(line)


class GameStats:
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True
        # Рекорд не должен сбрасываться.
        self.high_score = 0
        self.high = hi_score
        self.high_score = self.high

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def update_high_score(self):
        if self.high_score > self.high:
            with open('high_score.txt', 'w') as fp:
                fp.write(str(self.high_score))
