import pygame

from ui import UI
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

        self.ui = UI()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], [self.visible_sprites, self.attack_sprites],
                                         self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

    def custom_draw(self):
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect)
