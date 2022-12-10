import random

import pygame

from code.library.Resources import Resources
from code.level.particles.Particle import Particle


class FireParticle(Particle):
    def __init__(self, pos, colors=['#ffffff', '#fee761', '#feae34', '#f77622', '#e43b44', '#3e2731']):
        super().__init__()
        self.__sprite_type = 'particle'

        self.__mask_circle_32 = Resources().get_sprite('/masks/circle_32.png')
        self.__image = self.__mask_circle_32.copy()
        self.__image.set_alpha(0)  # para não desenhar a partícula ainda não configurada
        self.rect = self.__image.get_rect(center=pos)

        self.__size = 16 * random.randint(100, 150) / 100
        self.__colors = colors
        self.__color_index = 0

    @property
    def sprite_type(self):
        return self.__sprite_type

    @property
    def size(self):
        return self.__size

    @property
    def colors(self):
        return self.__colors

    @property
    def color_index(self):
        return self.__color_index

    def animate(self):
        if self.inner_timer % 4 == 0:
            # diminuir e mover a partícula
            self.__size = self.__size - random.randint(1, 3)
            self.rect.centery -= random.randint(1, 4)

        if self.__color_index < len(self.colors) - 1:
            # não permitir a cor inicial ficar por muito tempo
            if self.__size < 14 and self.__color_index == 0:
                self.__color_index += 1

            # lógica de próxima cor
            if random.randint(0, 4) == 2:
                self.__color_index += 1

        if self.__size <= 4:
            self.kill()

        self.__image = pygame.transform.scale(self.__mask_circle_32, (self.__size, self.__size))
        circle = pygame.Surface(self.__image.get_size())
        circle.fill(self.colors[self.__color_index])
        self.rect = circle.get_rect(center=self.rect.center)
        self.__image.set_alpha(255)
        self.__image.blit(circle, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    @property
    def image(self):
        return self.__image
