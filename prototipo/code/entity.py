import math

import pygame.sprite


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, sprite_type):
        super().__init__(groups)
        self._sprite_type = sprite_type
        self._direction = pygame.math.Vector2()

    @property
    def sprite_type(self):
        return self._sprite_type
    
    @sprite_type.setter
    def sprite_type(self, value):
        self._sprite_type = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction):
        self._direction = direction

    def move(self, speed, collision_hitbox_name='hitbox'):
        # o collision_hitbox_name é utilizado pelo DamageArea para escolher colidir somente com a
        # hitbox menor (smaller_hitbox) dos Tiles

        if self.direction.magnitude() != 0:
            # manter a velocidade caso o player esteja indo em na diagonal
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        collided = self.collision('horizontal', collision_hitbox_name)
        self.hitbox.y += self.direction.y * speed
        collided = self.collision('vertical', collision_hitbox_name) or collided
        # manter a hitbox nos pés da entidade
        self.rect.centerx = self.hitbox.centerx
        self.rect.bottom = self.hitbox.bottom
        return not collided

    def collision(self, direction, hitbox_name):
        # confira o move() para informações sobre o hitbox_name

        collided = False
        # colisão horizontal
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite != self and getattr(sprite, hitbox_name).colliderect(self.hitbox):
                    collided = True
                    if self._direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self._direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        # colisão vertical
        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite != self and getattr(sprite, hitbox_name).colliderect(self.hitbox):
                    collided = True
                    if self._direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self._direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
        return collided

    def wave_value(self):
        # utilizado como o alpha do efeito de flickering (piscando) quando a entidade recebe dano
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
