import random

import pygame

from entity import Entity
from particles import FireSource
from settings import TILESIZE


class EnemyDamageArea(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage=0, speed=0, direction=pygame.math.Vector2(),
                 destroy_on_impact=False,
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=6000, particle_spawners=[], hit_sound=None):
        super().__init__(groups, 'enemy_damage_area')
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

        self.particle_spawners = particle_spawners
        self.hit_sound = hit_sound

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

            if self.hit_sound is not None:
                self.hit_sound.play()

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

        for particle_spawner in self.particle_spawners:
            particle_spawner.rect.center = self.rect.center

    def kill(self):
        # apagar os particle spawners
        for particle_spawner in self.particle_spawners:
            if isinstance(particle_spawner, FireSource):
                # fazer uma "explosão" de fogo ao destruir
                for i in range(5, 15):
                    particle_spawner.offset = random.randint(16, 32)
                    particle_spawner.update()
            particle_spawner.kill()
        super().kill()
