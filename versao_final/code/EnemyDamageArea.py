import random

import pygame

from code.Camera import Camera
from code.Entity import Entity
from code.GroupManager import GroupManager
from code.Particles import FireSource, BloodSource
from code.Settings import TILESIZE


class EnemyDamageArea(Entity):
    def __init__(self, pos, damage=0, speed=0, direction=pygame.math.Vector2(),
                 destroy_on_impact=False,
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=60, damage_time=0,
                 particle_spawners=[],
                 hit_sound=None,
                 blood_on_kill=False,
                 fade_out_step=0,
                 screen_shake_on_kill=False):
        super().__init__('enemy_damage_area')
        self.__group_manager = GroupManager()
        self.__group_manager.add_to_attacks(self)
        self.image = surface
        self.rect = self.image.get_rect(center=pos)
        self.__hitbox = self.rect

        self.__damage = damage
        self.__speed = speed
        self.direction = direction
        self.__destroy_on_impact = destroy_on_impact
        self.__obstacle_sprites = self.__group_manager.tile_sprites
        self.__particle_spawners = particle_spawners

        self.__blood_on_kill = blood_on_kill
        self.__screen_shake_on_kill = screen_shake_on_kill
        self.__fade_out_step = fade_out_step
        self.__destroy_time = destroy_time
        self.__damage_time = damage_time if damage_time != 0 else destroy_time

        self.__destroy_timer = 0

        self.__hit_sound = hit_sound

    def enemy_collision(self):
        if not self.__damage_time > 0:
            # dar dano somente enquanto o damage time for maior que 0
            return

        collision_sprites = pygame.sprite.spritecollide(self, self.__group_manager.enemy_sprites, False)
        if collision_sprites:
            for target_sprite in collision_sprites:
                if not target_sprite.vulnerable:  # pular os inimigos que não estão vulneráveis
                    continue

                try:
                    # evitar exceção caso o arquivo de som não exista
                    self.hit_sound.play() 
                except Exception:
                    pass

                target_sprite.damage(self.__damage)
                if target_sprite.health <= 0:
                    target_sprite.check_death()

                    if self.__blood_on_kill:
                        BloodSource(collision_sprites[0].rect.center, self.direction)
                    if self.__screen_shake_on_kill:
                        Camera().shake()

                if self.__destroy_on_impact:  # ataque dá dano em só um inimigo
                    self.kill()
                    break

    def update(self):
        self.enemy_collision()
        # movimento
        self.image.set_alpha(self.image.get_alpha() - self.__fade_out_step)
        if self.__speed != 0:
            moved = self.move(self.__speed, 'smaller_hitbox')
            if not moved:
                # projétil colidiu com algum obstáculo
                self.kill()

            for particle_spawner in self.__particle_spawners:
                particle_spawner.rect.center = self.rect.center + self.direction * self.speed

        # tempo enquanto vai dar dano
        if self.__damage_time > 0:
            self.__damage_time -= 1

        # destruir após um tempo
        self.__destroy_timer += 1
        if self.__destroy_timer >= self.__destroy_time:
            self.kill()

    def kill(self):
        # apagar os particle spawners
        for particle_spawner in self.__particle_spawners:
            if isinstance(particle_spawner, FireSource):
                # fazer uma "explosão" de fogo ao destruir
                for i in range(5, 15):
                    particle_spawner.offset = random.randint(16, 32)
                    particle_spawner.update()
            particle_spawner.kill()
        super().kill()

    @property
    def hitbox(self):
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, value):
        self.__hitbox = value

    @property
    def damage(self):
        return self.__damage

    @property
    def speed(self):
        return self.__speed

    @property
    def destroy_on_impact(self):
        return self.__destroy_on_impact

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def particle_spawners(self):
        return self.__particle_spawners

    @property
    def blood_on_kill(self):
        return self.__blood_on_kill

    @property
    def fade_out_step(self):
        return self.__fade_out_step

    @property
    def destroy_time(self):
        return self.__destroy_time

    @property
    def damage_time(self):
        return self.__damage_time

    @property
    def destroy_timer(self):
        return self.__destroy_timer

    @property
    def hit_sound(self):
        return self.__hit_sound
