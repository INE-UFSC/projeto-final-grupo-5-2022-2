import random

import pygame

from code.GroupManager import GroupManager
from code.particles.BloodParticle import BloodParticle
from code.particles.ParticleSource import ParticleSource


class BloodSource(ParticleSource):
    def __init__(self, pos, direction, blood_speed=32, min_particles=8, max_particles=12):
        super().__init__(pos)
        self.__obstacle_sprites = GroupManager().tile_sprites
        self.__pos = pos
        self.__direction = direction
        self.__offset = 25
        self.__blood_speed = blood_speed
        self.__min_particles = min_particles
        self.__max_particles = max_particles

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def pos(self):
        return self.__pos

    @property
    def direction(self):
        return self.__direction

    @property
    def offset(self):
        return self.__offset

    @property
    def blood_speed(self):
        return self.__blood_speed

    @property
    def min_particles(self):
        return self.__min_particles

    @property
    def max_particles(self):
        return self.__max_particles

    def update(self):
        for i in range(random.randint(self.min_particles, self.max_particles)):
            direction = pygame.math.Vector2(self.direction.x, self.direction.y)
            direction.x += random.randint(-self.offset, self.offset) / 100
            direction.y += random.randint(-self.offset, self.offset) / 100
            direction.normalize()
            particle = BloodParticle(self.pos, direction, speed=self.blood_speed)
            self.group_manager.add_to_particles(particle)
        self.kill()
