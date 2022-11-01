import math
import random
from abc import ABC, abstractmethod

import pygame
import pygame.sprite

from utils import load_sprite


class ParticleSource(pygame.sprite.Sprite, ABC):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'particle_source'
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect(center=pos)


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
        self.offset = 16

    def update(self):
        # criar as partículas de fogo
        for i in range(random.randint(1, 3)):
            x_offset = random.randint(-self.offset, self.offset)
            y_offset = random.randint(-self.offset, self.offset)
            FireParticle((self.rect.centerx + x_offset, self.rect.centery + y_offset), self.groups())


class FireParticle(Particle):
    def __init__(self, pos, groups, colors=['#ffffff', '#fee761', '#feae34', '#f77622', '#e43b44', '#3e2731']):
        super().__init__(groups)
        self.sprite_type = 'particle'

        self.mask_circle_32 = load_sprite('/mask/circle_32.png')
        self.image = self.mask_circle_32.copy()
        self.image.set_alpha(0)  # para não desenhar a partícula ainda não configurada
        self.rect = self.image.get_rect(center=pos)

        self.size = 16 * random.randint(100, 150) / 100
        self.colors = colors
        self.color_index = 0

    def animate(self):
        if self.inner_timer % 4 == 0:
            # diminuir e mover a partícula
            self.size = self.size - random.randint(1, 3)
            self.rect.centery -= random.randint(1, 4)

        if self.color_index < len(self.colors) - 1:
            # não permitir a cor inicial ficar por muito tempo
            if self.size < 14 and self.color_index == 0:
                self.color_index += 1

            # lógica de próxima cor
            if random.randint(0, 4) == 2:
                self.color_index += 1

        if self.size <= 4:
            self.kill()

        self.image = pygame.transform.scale(self.mask_circle_32, (self.size, self.size))
        circle = pygame.Surface(self.image.get_size())
        circle.fill(self.colors[self.color_index])
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
        self.sprite_type = 'light'

        self.mask_circle_32 = load_sprite('/mask/circle_32.png')
        self.image = self.mask_circle_32.copy()
        self.image.set_alpha(0)  # para não desenhar a partícula ainda não configurada
        self.rect = self.image.get_rect(center=pos)

        self.original_diameter = diameter
        self.size = (self.original_diameter, self.original_diameter)
        self.color = color
        self.diff = 0
        self.shrink_mag = shrink_mag
        self.grow_mag = grow_mag

    def animate(self):
        if self.inner_timer % 10 == 0:
            sin = math.sin(self.inner_timer / 10)
            self.diff = sin * self.shrink_mag if sin < 0 else sin * self.grow_mag
        new_diameter = max(1, self.original_diameter + self.diff)
        self.size = (new_diameter, new_diameter)

        self.image = pygame.transform.scale(self.mask_circle_32, self.size)
        circle = pygame.Surface(self.image.get_size())
        circle.fill(self.color)
        self.rect = circle.get_rect(center=self.rect.center)
        self.image.set_alpha(50)
        self.image.blit(circle, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class BloodSource(ParticleSource):
    def __init__(self, pos, groups, obstacle_sprites, direction, blood_speed=32, min_particles=8, max_particles=12):
        super().__init__(pos, groups)
        self.obstacle_sprites = obstacle_sprites
        self.pos = pos
        self.direction = direction
        self.offset = 25
        self.blood_speed = blood_speed
        self.min_particles = min_particles
        self.max_particles = max_particles

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
        self.sprite_type = 'on_ground'
        self.obstacle_sprites = obstacle_sprites

        self.mask_circle_32 = load_sprite('/mask/circle_32.png')
        self.image = self.mask_circle_32.copy()
        self.image.set_alpha(0)  # para não desenhar a partícula ainda não configurada
        self.rect = self.image.get_rect(center=pos)

        self.direction = direction
        self.size = 32 * random.randint(25, 150) / 100
        self.color = color
        self.speed = speed * random.randint(100, 150) / 100

    def animate(self):
        # diminuir e mover a partícula
        if self.inner_timer % 2 == 0:
            if self.inner_timer >= 5 and self.speed > 0:
                self.size = max(1, self.size - random.randint(1, 2))
                self.speed = max(0, self.speed - random.randint(2, 12))
            else:
                self.speed = max(0, self.speed - random.randint(4, 16))

            self.rect.center += self.direction * self.speed

        # calcular próximo alpha
        new_alpha = self.image.get_alpha() - 1 if self.inner_timer > 100 else 255

        # destruição
        if self.size <= 4 or new_alpha == 0:
            self.kill()

        self.image = pygame.transform.scale(self.mask_circle_32, (self.size, self.size))
        self.image.set_alpha(new_alpha)
        circle = pygame.Surface(self.image.get_size())
        circle.fill(self.color)
        self.rect = circle.get_rect(center=self.rect.center)
        self.image.blit(circle, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
