import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.math import Vector2

import random
from dataclasses import dataclass

@dataclass
class Movable:
    surface: Surface
    rect: Rect
    move_by: Vector2

pygame.init()

FPS = pygame.time.Clock()

WIDTH = 1200
HEIGHT = 800

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0,0,255)
COLOR_GREEN = (0,255,0)
PLAYER_SIZE = (20, 20)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player = pygame.Surface(PLAYER_SIZE)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()

player_move_down = [0,1]
player_move_up = [0,-1]
player_move_right = [1,0]
player_move_left = [-1,0]

def create_enemy():
    enemy_size = (30,30)
    enemy = pygame.Surface(enemy_size)
    enemy.fill(COLOR_BLUE)
    enemy_rect = pygame.Rect(WIDTH, random.randint(0, HEIGHT), *enemy_size)
    enemy_move = [random.randint(-6, -1), 0]
    return Movable(enemy, enemy_rect, enemy_move)

def create_bonus():
    bonus_size = (25,25)
    bonus = pygame.Surface(bonus_size)
    bonus.fill(COLOR_GREEN)
    bonus_rect = pygame.Rect(random.randint(0, WIDTH), 0, *bonus_size)
    bonus_move = [0, random.randint(2, 4)]
    return Movable(bonus, bonus_rect, bonus_move)

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2

pygame.time.set_timer(CREATE_ENEMY, random.randint(1000, 2000))
pygame.time.set_timer(CREATE_BONUS, random.randint(2000, 3000))

enemies = []
bonuses = []

playing = True

while playing:
    FPS.tick(240)
    for event in pygame.event.get():
        if event.type == QUIT: playing = False
        if event.type == CREATE_ENEMY: enemies.append(create_enemy())
        if event.type == CREATE_BONUS: bonuses.append(create_bonus())
    
    main_display.fill(COLOR_BLACK)

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT: player_rect = player_rect.move(player_move_down)
    if keys[K_UP] and player_rect.top > 0: player_rect = player_rect.move(player_move_up)
    if keys[K_RIGHT] and player_rect.right < WIDTH: player_rect = player_rect.move(player_move_right)
    if keys[K_LEFT] and player_rect.left > 0: player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy.rect = enemy.rect.move(enemy.move_by)
        main_display.blit(enemy.surface, enemy.rect)

    for bonus in bonuses:
        bonus.rect = bonus.rect.move(bonus.move_by)
        main_display.blit(bonus.surface, bonus.rect)

    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy.rect.left < 0: enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if (bonus.rect.bottom > HEIGHT): bonuses.pop(bonuses.index(bonus))
