import random

import pygame

from entity import Entity
from particles import FireSource, BloodSource
from settings import TILESIZE


class EnemyDamageArea(Entity):
    def __init__(self, pos, groups, obstacle_sprites, damage=0, speed=0, direction=pygame.math.Vector2(),
                 destroy_on_impact=False,
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=6000, particle_spawners=[], hit_sound=None,
                 blood_on_kill=False, fade_out_step = 0):
        super().__init__(groups, 'enemy_damage_area')
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

        self._damage = damage
        self._speed = speed
        self._direction = direction
        self._destroy_on_impact = destroy_on_impact
        self._obstacle_sprites = obstacle_sprites
        self._particle_spawners = particle_spawners

        self.__blood_on_kill = blood_on_kill
        self.__fade_out_step = fade_out_step
        self.__destroy_time = destroy_time

        self.__destroy_timer = 0
        self.__is_enabled = True

        self.hit_sound = hit_sound

    @property
    def hitbox(self):
        return self._hitbox

    @hitbox.setter
    def hitbox(self, value):
        self._hitbox = value

    @property
    def damage(self):
        return self._damage

    @property
    def speed(self):
        return self._speed

    @property
    def destroy_on_impact(self):
        return self._destroy_on_impact

    @property
    def obstacle_sprites(self):
        return self._obstacle_sprites

    @property
    def particle_spawners(self):
        return self._particle_spawners

    def enemy_collision(self, player, attackable_group):
        collision_sprites = pygame.sprite.spritecollide(self, attackable_group, False)
        if collision_sprites:
            for target_sprite in collision_sprites:
                if not target_sprite.vulnerable:  # pular os inimigos que não estão vulneráveis
                    continue

                if self.hit_sound is not None:
                    self.hit_sound.play()

                target_sprite.damage(self._damage, player)
                if target_sprite.health <= 0:
                    target_sprite.check_death(player)
                    if self.__blood_on_kill:
                        BloodSource(collision_sprites[0].rect.center, self.groups()[0], self._obstacle_sprites,
                                    self._direction)

                if self._destroy_on_impact:  # ataque dá dano em só um inimigo
                    self.kill()
                    break

    def update(self):
        # movimento
        self.image.set_alpha(self.image.get_alpha() - self.__fade_out_step)
        if self._speed != 0:
            moved = self.move(self._speed, 'smaller_hitbox')
            if not moved:
                # projétil colidiu com algum obstáculo
                self.kill()

        # destruir após um tempo
        self.__destroy_timer += 1
        if self.__destroy_timer >= self.__destroy_time:
            self.kill()

        for particle_spawner in self._particle_spawners:
            particle_spawner.rect.center = self.rect.center

    def kill(self):
        # apagar os particle spawners
        for particle_spawner in self._particle_spawners:
            if isinstance(particle_spawner, FireSource):
                # fazer uma "explosão" de fogo ao destruir
                for i in range(5, 15):
                    particle_spawner.offset = random.randint(16, 32)
                    particle_spawner.update()
            particle_spawner.kill()
        super().kill()
