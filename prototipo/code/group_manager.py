import pygame

from code.camera import YSortCameraGroup
from code.singleton import Singleton


class GroupManager(Singleton):
    def __init__(self) -> None:
        super().__init__()
        self.__visible_sprites = YSortCameraGroup()
        self.__obstacle_sprites = pygame.sprite.Group()
        self.__attack_sprites = pygame.sprite.Group()
        self.__attackable_sprites = pygame.sprite.Group()

    @property
    def visible_sprites(self):
        return self.__visible_sprites

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def attack_sprites(self):
        return self.__attack_sprites

    @property
    def attackable_sprites(self):
        return self.__attackable_sprites

    def clear_all_groups(self):
        self.__visible_sprites.empty()
        self.__obstacle_sprites.empty()
        self.__attack_sprites.empty()
        self.__attackable_sprites.empty()
