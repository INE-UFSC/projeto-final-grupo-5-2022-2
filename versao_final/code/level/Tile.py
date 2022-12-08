import pygame

from code.library.Resources import Resources
from code.library.Settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, tile_number=''):
        super().__init__()
        self.__sprite_type = 'tile'
        self.__tile_number = tile_number
        # TODO: Ajustar a parte do offset
        self.__image = Resources().get_sprite(f'/tiles/{self.__tile_number}.png') if len(
            self.__tile_number) > 0 else pygame.Surface((TILESIZE, TILESIZE))
        self.__rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.inflate(X_OFFSET.get(self.__tile_number, -16), Y_OFFSET.get(self.__tile_number, -16))
        self.__hitbox.bottom = self.__rect.bottom
        small_hitbox_offset = SMALL_HITBOX_OFFSET.get(self.__tile_number, 0)
        self.__smaller_hitbox = self.rect.inflate(-16 + small_hitbox_offset, -10 + small_hitbox_offset)
        self.__smaller_hitbox.center = self.rect.center

    @property
    def sprite_type(self):
        return self.__sprite_type

    @property
    def tile_number(self):
        return self.__tile_number

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
