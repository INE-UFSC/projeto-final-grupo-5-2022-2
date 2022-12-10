from abc import ABC

import pygame

from code.level.GroupManager import GroupManager


class ParticleSource(pygame.sprite.Sprite, ABC):
    def __init__(self, pos):
        super().__init__()
        self.__group_manager = GroupManager()
        self.__sprite_type = 'particle_source'
        self.__image = pygame.Surface((1, 1))
        self.__rect = self.__image.get_rect(center=pos)

    @property
    def group_manager(self):
        return self.__group_manager

    @property
    def sprite_type(self):
        return self.__sprite_type

    @sprite_type.setter
    def sprite_type(self, sprite_type):
        self.__sprite_type = sprite_type

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect
