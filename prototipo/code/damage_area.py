from abc import ABC

import pygame

from entity import Entity
from settings import TILESIZE


class DamageArea(Entity, ABC):
    def __init__(self, groups):
        super().__init__(groups)


class EnemyDamageArea(DamageArea):
    def __init__(self, pos, groups, obstacle_sprites, speed=0, direction=pygame.math.Vector2(),
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=6000):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        self.speed = speed
        self.direction = direction
        self.obstacle_sprites = obstacle_sprites

        self.creation_time = pygame.time.get_ticks()
        self.destroy_time = destroy_time

    # sobreescrever a colisão para colidir com a hitbox menor das paredes
    def collision(self, direction):
        collided = False
        # colisão horizontal
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.smaller_hitbox.colliderect(self.hitbox):
                    collided = True
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.smaller_hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.smaller_hitbox.right
        # colisão vertical
        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.smaller_hitbox.colliderect(self.hitbox):
                    collided = True
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.smaller_hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.smaller_hitbox.bottom
        return collided

    def update(self):
        if self.speed != 0:
            moved = self.move(self.speed)
            if not moved:
                # projétil colidiu com algum obstáculo
                self.kill()

        # destruir após um tempo
        current_time = pygame.time.get_ticks()
        if current_time - self.creation_time >= self.destroy_time:
            self.kill()


class PlayerDamageArea(DamageArea):
    def __init__(self):
        pass