import pygame

from code.utils import load_sprite


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.__sprite_type = 'tile'
        self.__image = load_sprite('/test/rock.png')
        self.__rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.inflate(0, -16)
        self.__smaller_hitbox = self.rect.inflate(-16, -26)
        self.__smaller_hitbox.y = self.rect.y

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
