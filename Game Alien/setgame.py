import pygame

class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""

    def __init__(self):
        """Инициализирует настройки игры."""
        # параметры экрана
        self.screen_width = 1300
        self.screen_height = 800
        self.image = pygame.image.load('blue_bg.png')
        # настройки корабля
        self.ship_speed_factor = 20
        # Параметры пули
        self.bullet_speed_factor = 15
        self.bullet_width = 5
        self.bullet_height = 25
        self.bullet_color = 255, 0,  0
        self.bullets_allowed = 30
        # Настройки пришельцев
        self.alien_speed_factor = 3
        # Темп ускорения игры
        self.speedup_scale = 1.2
        # Темп роста стоимости пришельцев
        self.score_scale = 1.5
        self.initialize_dynamic_settings()
        self.initialize_dynamic_settings()
        # величиной снижения флота
        self.fleet_drop_speed = 20
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        self.ship_limit = 3
        self.high_score = 0

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""

        self.ship_speed_factor = 15
        self.bullet_speed_factor = 20
        self.alien_speed_factor = 3
        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1
        # Подсчет очков
        self.alien_points = 10

    def increase_speed(self):
        """Увеличивает настройки скорости."""

        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
