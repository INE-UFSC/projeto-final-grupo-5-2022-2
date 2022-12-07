import math

import pygame

from code.Resources import Resources
from code.particles.Particle import Particle


class LightParticle(Particle):
    def __init__(self, pos, diameter, color, shrink_mag=16, grow_mag=16):
        super().__init__()
        self.__sprite_type = 'light'

        self.__mask_circle_32 = Resources().get_sprite('/masks/circle_32.png')
        self.image = self.__mask_circle_32.copy()
        self.image.set_alpha(0)  # para não desenhar a partícula ainda não configurada
        self.rect = self.image.get_rect(center=pos)

        self.__original_diameter = diameter
        self.__size = (self.original_diameter, self.original_diameter)
        self.__color = color
        self.__diff = 0
        self.__shrink_mag = shrink_mag
        self.__grow_mag = grow_mag

    @property
    def sprite_type(self):
        return self.__sprite_type

    @property
    def mask_circle(self):
        return self.__mask_circle_32

    @property
    def original_diameter(self):
        return self.__original_diameter

    @property
    def size(self):
        return self.__size

    @property
    def color(self):
        return self.__color

    @property
    def diff(self):
        return self.__diff

    @property
    def shrink_mag(self):
        return self.__shrink_mag

    @property
    def grow_mag(self):
        return self.__grow_mag

    def animate(self):
        if self.inner_timer % 10 == 0:
            sin = math.sin(self.inner_timer / 10)
            self.__diff = sin * self.shrink_mag if sin < 0 else sin * self.grow_mag
        new_diameter = max(1, self.original_diameter + self.__diff)
        self.__size = (new_diameter, new_diameter)

        self.image = pygame.transform.scale(self.__mask_circle_32, self.__size)
        circle = pygame.Surface(self.image.get_size())
        circle.fill(self.color)
        self.rect = circle.get_rect(center=self.rect.center)
        self.image.set_alpha(50)
        self.image.blit(circle, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
