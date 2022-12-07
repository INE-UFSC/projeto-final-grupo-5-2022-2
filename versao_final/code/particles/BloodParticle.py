import random

import pygame

from code.GroupManager import GroupManager
from code.Resources import Resources
from code.particles.Particle import Particle


class BloodParticle(Particle):
    def __init__(self, pos, direction, color='#e43b44', speed=32):
        super().__init__()
        self.__sprite_type = 'on_ground'
        self.__obstacle_sprites = GroupManager().tile_sprites

        self.__mask_circle_32 = Resources().get_sprite('/masks/circle_32.png')
        self.image = self.__mask_circle_32.copy()
        self.image.set_alpha(0)  # para não desenhar a partícula ainda não configurada
        self.rect = self.image.get_rect(center=pos)

        self.__direction = direction
        self.__size = 32 * random.randint(25, 150) / 100
        self.__color = color
        self.__speed = speed * random.randint(100, 150) / 100

    @property
    def sprite_type(self):
        return self.__sprite_type

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def mask_circle(self):
        return self.__mask_circle_32

    @property
    def direction(self):
        return self.__direction

    @property
    def size(self):
        return self.__size

    @property
    def color(self):
        return self.__color

    @property
    def speed(self):
        return self.__speed

    def animate(self):
        if self.__speed == 0:
            return

        # diminuir e mover a partícula
        if self.inner_timer % 2 == 0:
            if self.inner_timer >= 5 and self.__speed > 0:
                self.__size = max(1, self.__size - random.randint(1, 2))
                self.__speed = max(0, self.__speed - random.randint(2, 12))
            else:
                self.__speed = max(0, self.__speed - random.randint(4, 16))

            self.rect.center += self.direction * self.__speed

        # destruição
        if self.__size <= 4:
            self.kill()

        self.image = pygame.transform.scale(self.__mask_circle_32, (self.__size, self.__size))
        self.image.set_alpha(200)
        circle = pygame.Surface(self.image.get_size())
        circle.fill(self.color)
        self.rect = circle.get_rect(center=self.rect.center)
        self.image.blit(circle, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
