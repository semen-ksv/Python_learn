import sys
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш."""
    # считывание при нажатии клавиш
    if event.key == pygame.K_RIGHT:
        # ship.rect.centerx += 1
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # # Создание новой пули и включение ее в группу bullets.
        # if len(bullets) < ai_settings.bullets_allowed:  # c ограничением количества выпущеных пуль
        #     new_bullet = Bullet(ai_settings, screen, ship)
        #     bullets.add(new_bullet)
        fire_bullet(ai_settings, screen, ship, bullets)  # вышеуказнное заменено на функцию
    elif event.key == pygame.K_q:
        #выход по клавише q
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Выпускает пулю, если максимум еще не достигнут."""
    # Создание новой пули и включение ее в группу bullets.
    if len(bullets) < ai_settings.bullets_allowed:    # c ограничением количества выпущеных пуль
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш."""
    # считывание при отжатии клавиш
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, ship, bullets):
    """Обрабатывает нажатия клавиш и события мыши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # # считывание при нажатии клавиш
            # if event.key == pygame.K_RIGHT:       #перенесенов в фунцию eck_keydown_events
            #     #ship.rect.centerx += 1
            #     ship.moving_right = True
            # if event.key == pygame.K_LEFT:
            #     ship.moving_left = True
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            # считывание при отжатии клавиш
            # if event.key == pygame.K_RIGHT:       #перенесенов в фунцию check_keyup_events
            #     ship.moving_right = False
            # if event.key == pygame.K_LEFT:
            #     ship.moving_left = False
            check_keyup_events(event, ship)

def update_screen(ai_settings, screen, ship,  aliens, bullets):
    """Обновляет изображения на экране и отображает новый экран."""
    # заливка фона, при каждом проходе цикла, цветом для удаления следа картинки
    screen.blit(ai_settings.image, (0, 0))
    # Все пули выводятся позади изображений корабля и пришельцев.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # alien.blitme()  # Чтобы пришелец появился на экране
    aliens.draw(screen)     # прорисовка флота пришельцев
    # Отображение последнего прорисованного экрана.
    pygame.display.flip()


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    """Обновляет позиции пуль и уничтожает старые пули."""
    # Обновление позиций пуль.
    bullets.update()
    # Проверка попаданий в пришельцев.
    # При обнаружении попадания удалить пулю и пришельца.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
    # Уничтожение существующих пуль и создание нового флота.
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

    # Удаление пуль, вышедших за край экрана
    for bullet in bullets.copy():  # копию группы
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def get_number_aliens_x(ai_settings, alien_width):
    """Вычисляет количество пришельцев в ряду."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_row(ai_settings, ship_height, alien_height):
    """Определяет количество рядов, помещающихся на экране."""
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_row = int(available_space_y / (2*alien_height))
    return number_row

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Создает пришельца и размещает его в ряду."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 1.5 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Создает флот пришельцев."""
    # Создание пришельца и вычисление количества пришельцев в ряду.
    # Интервал между соседними пришельцами равен одной ширине пришельца.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_row = get_number_row(ai_settings, ship.rect.height, alien.rect.height)

    # Создание первого ряда пришельцев.
    # создание флота пришельцев
    for row_number in range(number_row):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_fleet_edges(ai_settings, aliens):
    """Реагирует на достижение пришельцем края экрана."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Опускает весь флот и меняет направление флота."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, aliens):
    """Проверяет, достиг ли флот края экрана, после чего обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()