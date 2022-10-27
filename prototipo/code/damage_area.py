from abc import ABC

import pygame

from entity import Entity
from settings import TILESIZE


class DamageArea(Entity, ABC):
    def __init__(self, groups):
        super().__init__(groups)


class EnemyDamageArea(DamageArea):
    def __init__(self, pos, groups, obstacle_sprites, damage=0, speed=0, direction=pygame.math.Vector2(),
                 destroy_on_impact=False,
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=6000):
        super().__init__(groups)
        self.sprite_type = 'enemy_damage_area'
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        self.damage = damage
        self.speed = speed
        self.direction = direction
        self.destroy_on_impact = destroy_on_impact
        self.obstacle_sprites = obstacle_sprites

        self.creation_time = pygame.time.get_ticks()
        self.destroy_time = destroy_time

    def enemy_collision(self, player, attackable_group):
        collision_sprites = pygame.sprite.spritecollide(self, attackable_group, False)
        if collision_sprites:
            if self.destroy_on_impact:
                # ataque só dá dano em 1 inimigo
                collision_sprites[0].damage(self.damage, player)
                self.kill()
            else:
                # ataque dá dano em vários inimigos
                for target_sprite in collision_sprites:
                    target_sprite.damage(self.damage, player)

    def update(self):
        # movimento
        if self.speed != 0:
            moved = self.move(self.speed, 'smaller_hitbox')
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
