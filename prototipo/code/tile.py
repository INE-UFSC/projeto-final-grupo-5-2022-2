import pygame

from code.settings import *
from code.sprite_manager import SpriteManager


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, tile_number=''):
        super().__init__(groups)
        self.__sprite_type = 'tile'
        if len(tile_number) != 0:
            self.__image = SpriteManager().get_sprite(f'/objects/{tile_number}.png')
        else:
            self.__image = pygame.Surface((TILESIZE, TILESIZE))
        self.__rect = self.image.get_rect(topleft=pos)
        x_offset = X_OFFSET.get(tile_number, -16)
        y_offset = Y_OFFSET.get(tile_number, -16)
        self.__hitbox = self.rect.inflate(x_offset, y_offset)
        self.__hitbox.bottom = self.__rect.bottom
        self.__smaller_hitbox = self.rect.inflate(-16 + x_offset, -10 + y_offset)
        self.__smaller_hitbox.center = self.rect.center

    @property
    def sprite_type(self):
        return self.__sprite_type

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect

    @property
    def hitbox(self):
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, hitbox):
        self.__hitbox = hitbox

    @property
    def smaller_hitbox(self):
        return self.__smaller_hitbox

    @smaller_hitbox.setter
    def smaller_hitbox(self, smaller_hitbox):
        self.__smaller_hitbox = smaller_hitbox
