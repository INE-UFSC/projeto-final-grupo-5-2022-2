import math

import pygame

from damage_area import EnemyDamageArea
from player import Player
from settings import *
from tile import Tile


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        # criar o mapa
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacle_sprites, self.create_attack)

    def create_attack(self):
        # centralizar a bola de fogo no player
        sprite = pygame.image.load('../graphics/test/fireball.png').convert_alpha()
        pos = (self.player.rect.centerx - (sprite.get_rect().width // 2), self.player.rect.centery - (sprite.get_rect().height // 2))
        # calcular direção do projétil
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(self.player.rect.centery - mouse_pos[1], self.player.rect.centerx - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # criar o projétil
        EnemyDamageArea(pos, [self.visible_sprites, self.attack_sprites], self.obstacle_sprites,
                        speed=10, direction=direction,
                        surface=sprite)

    def run(self):
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect)
