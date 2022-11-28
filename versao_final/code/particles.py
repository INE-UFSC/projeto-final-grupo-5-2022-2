import math
import random
from abc import ABC, abstractmethod

import pygame
import pygame.sprite

from code.resources import Resources


class ParticleSource(pygame.sprite.Sprite, ABC):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.__sprite_type = 'particle_source'
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect(center=pos)

    @property
    def sprite_type(self):
        return self.__sprite_type

    @sprite_type.setter
    def sprite_type(self, sprite_type):
        self.__sprite_type = sprite_type


class Particle(pygame.sprite.Sprite, ABC):
    def __init__(self, groups):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.inner_timer = 0  # um timer interno é mais suave que utilizar os ticks do pygame

    @abstractmethod
    def animate(self):
        pass

    def update(self):
        self.inner_timer += 1
        self.animate()


class FireSource(ParticleSource):
    def __init__(self, pos, groups):
        super().__init__(pos, groups)
        self.__offset = 16

    @property
    def offset(self):
        return self.__offset

    @offset.setter
    def offset(self, offset):
        self.__offset = offset

    def update(self):
        # criar as partículas de fogo
        for i in range(random.randint(1, 3)):
            x_offset = random.randint(-self.offset, self.offset)
            y_offset = random.randint(-self.offset, self.offset)
            FireParticle((self.rect.centerx + x_offset, self.rect.centery + y_offset), self.groups())


class FireParticle(Particle):
    def __init__(self, pos, groups, colors=['#ffffff', '#fee761', '#feae34', '#f77622', '#e43b44', '#3e2731']):
        super().__init__(groups)
        self.__sprite_type = 'particle'

        self.__mask_circle_32 = Resources().get_sprite('/masks/circle_32.png')
        self.image = self.__mask_circle_32.copy()
        self.image.set_alpha(0)  # para não desenhar a partícula ainda não configurada
        self.rect = self.image.get_rect(center=pos)

        self.__size = 16 * random.randint(100, 150) / 100
        self.__colors = colors
        self.__color_index = 0

    @property
    def mask_circle_32(self):
        return self.__mask_circle_32

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

        self.image = pygame.transform.scale(self.__mask_circle_32, (self.__size, self.__size))
        circle = pygame.Surface(self.image.get_size())
        circle.fill(self.colors[self.__color_index])
        self.rect = circle.get_rect(center=self.rect.center)
        self.image.set_alpha(255)
        self.image.blit(circle, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class LightSource(ParticleSource):
    def __init__(self, pos, groups, outer_diameter=128, outer_color='#f77622', inner_diameter=96,
                 inner_color='#feae34'):
        super().__init__(pos, groups)
        self.particles = [LightParticle(pos, groups, outer_diameter, outer_color, 16, 16),
                          LightParticle(pos, groups, inner_diameter, inner_color, 64, 8)]

    def kill(self):
        for particle in self.particles:
            particle.kill()
        super().kill()

    def update(self):
        for particle in self.particles:
            particle.rect.center = self.rect.center


class LightParticle(Particle):
    def __init__(self, pos, groups, diameter, color, shrink_mag=16, grow_mag=16):
        super().__init__(groups)
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


class BloodSource(ParticleSource):
    def __init__(self, pos, groups, obstacle_sprites, direction, blood_speed=32, min_particles=8, max_particles=12):
        super().__init__(pos, groups)
        self.__obstacle_sprites = obstacle_sprites
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
            BloodParticle(self.pos, self.groups(), self.obstacle_sprites, direction, speed=self.blood_speed)
        self.kill()


class BloodParticle(Particle):
    def __init__(self, pos, groups, obstacle_sprites, direction, color='#e43b44', speed=32):
        super().__init__(groups)
        self.__sprite_type = 'on_ground'
        self.__obstacle_sprites = obstacle_sprites

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
        circle = pygame.Surface(self.image.get_size())
        circle.fill(self.color)
        self.rect = circle.get_rect(center=self.rect.center)
        self.image.blit(circle, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class AnimationParticle(Particle):
    def __init__(self, pos, groups, animation, animation_speed, destroy_on_end=False):
        super().__init__(groups)
        self.__sprite_type = 'particle'
        self.__animation = animation
        self.__animation_speed = animation_speed
        self.__frame_index = 0
        self.__destroy_on_end = destroy_on_end
        self.image = self.__animation[0]
        self.rect = self.image.get_rect(center=pos)

    @property
    def sprite_type(self):
        return self.__sprite_type

    def animate(self):
        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(self.__animation):
            if self.__destroy_on_end:
                self.kill()
            self.__frame_index = 0
        self.image = self.__animation[int(self.__frame_index)]
        self.rect = self.image.get_rect(center=self.rect.center)
