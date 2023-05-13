import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
from pygame.surface import Surface
from pygame.rect import Rect
from pygame.math import Vector2

import random
from dataclasses import dataclass

import os
import sys

def asset_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'assets/', relative_path)


@dataclass
class Object:
    surface: Surface
    rect: Rect

@dataclass
class Movable(Object):
    move_by: Vector2

    def move(self): self.rect = self.rect.move(self.move_by)

@dataclass
class Player(Object):
    player_image_index: int = 0

    def __init__(self, surface: Surface):
        self.surface = surface
        self.rect = self.surface.get_rect().move(10, HEIGHT / 2)

    def move_up(self):
        if self.rect.top > 0: self.rect = self.rect.move([0,-7])
    def move_down(self):
        if self.rect.bottom < HEIGHT: self.rect = self.rect.move([0,7])
    def move_left(self):
        if self.rect.left > 0: self.rect = self.rect.move([-7,0])
    def move_right(self):
        if self.rect.right < WIDTH: self.rect = self.rect.move([7,0])

    def anim(self):
        self.surface = pygame.image.load(os.path.join(GOOSE_ANIM_PATH, PLAYER_IMAGES[self.player_image_index]))
        self.player_image_index = (self.player_image_index + 1) % len(PLAYER_IMAGES)

pygame.init()

FPS = pygame.time.Clock()

WIDTH = 1200
HEIGHT = 800

COLOR_BLACK = (0,0,0)
FONT = pygame.font.SysFont("Verdana", 24)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load(asset_path('background.png')), (WIDTH, HEIGHT))
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

GOOSE_ANIM_PATH = asset_path('goose_anim')
PLAYER_IMAGES = os.listdir(GOOSE_ANIM_PATH)

player = Player(pygame.image.load(asset_path('player.png')).convert_alpha())

def create_enemy():
    enemy = pygame.image.load(asset_path('enemy.png')).convert_alpha()
    enemy_rect = pygame.Rect(WIDTH, random.randint(100, HEIGHT -100), *enemy.get_size())
    enemy_move = [random.randint(-8, -4), 0]
    return Movable(enemy, enemy_rect, enemy_move)

def create_bonus():
    bonus = pygame.image.load(asset_path('bonus.png')).convert_alpha()
    bonus_rect = pygame.Rect(random.randint(300, WIDTH - 300), 0, *bonus.get_size())
    bonus_move = [0, random.randint(2, 4)]
    return Movable(bonus, bonus_rect, bonus_move)

CREATE_ENEMY = pygame.USEREVENT + 1
CREATE_BONUS = pygame.USEREVENT + 2
CHANGE_IMAGE = pygame.USEREVENT + 3

pygame.time.set_timer(CREATE_ENEMY, random.randint(1000, 2000))
pygame.time.set_timer(CREATE_BONUS, random.randint(2000, 4000))
pygame.time.set_timer(CHANGE_IMAGE, random.randint(150, 300))

enemies = []
bonuses = []
score = 0

playing = True

while playing:
    FPS.tick(240)
    for event in pygame.event.get():
        if event.type == QUIT: playing = False
        if event.type == CREATE_ENEMY: enemies.append(create_enemy())
        if event.type == CREATE_BONUS: bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE: player.anim()
    
    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width(): bg_x1 = bg.get_width()
    if bg_x2 < -bg.get_width(): bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1,0))
    main_display.blit(bg, (bg_x2,0))

    keys = pygame.key.get_pressed()

    if keys[K_UP]: player.move_up()
    if keys[K_DOWN]: player.move_down()
    if keys[K_LEFT]: player.move_left()
    if keys[K_RIGHT]: player.move_right()

    for enemy in enemies:
        enemy.move()
        main_display.blit(enemy.surface, enemy.rect)

        if player.rect.colliderect(enemy.rect):
            playing = False

    for bonus in bonuses:
        bonus.move()
        main_display.blit(bonus.surface, bonus.rect)

        if player.rect.colliderect(bonus.rect):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player.surface, player.rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy.rect.right < 0: enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if (bonus.rect.top > HEIGHT): bonuses.pop(bonuses.index(bonus))
