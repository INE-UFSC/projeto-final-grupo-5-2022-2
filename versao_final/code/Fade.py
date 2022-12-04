import pygame

from code.Settings import *


class Fade(pygame.sprite.Sprite):
    def __init__(self, in_step=3, out_step=-2, alpha=0):
        super().__init__()
        self.__sprite_type = 'effect'
        self.__image = pygame.Surface((WIDTH, HEIGHT))
        self.__image.fill(COLOR_BLACK)
        self.__image.set_alpha(alpha)
        self.__rect = self.__image.get_rect()
        self.__in_step = in_step
        self.__out_step = out_step
        self.__animation = 'none'

    def fade_in(self):
        self.__animation = 'in'

    def fade_out(self):
        self.__animation = 'out'

    def animation_ended(self) -> bool:
        return self.__image.get_alpha() == 0 or self.__image.get_alpha() == 255

    def animate(self):
        if self.__animation == 'none':
            return
        fade_step = self.__in_step if self.__animation == 'in' else self.__out_step
        self.__image.set_alpha(self.__image.get_alpha() + fade_step)

    @property
    def sprite_type(self):
        return self.__sprite_type

    @property
    def image(self):
        return self.__image

    @property
    def rect(self):
        return self.__rect
