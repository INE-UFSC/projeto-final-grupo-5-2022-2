import pygame

from code.Settings import *
from code.damage.DamageArea import DamageArea


class PlayerDamageArea(DamageArea):
    def __init__(self, pos, damage=0, speed=0, direction=pygame.math.Vector2(),
                 destroy_on_impact=False,
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=60, damage_time=0,
                 particle_spawners=[],
                 hit_sound=None,
                 blood_on_kill=False,
                 fade_out_step=0,
                 screen_shake_on_kill=False):
        super().__init__(pos, damage, speed, direction, destroy_on_impact, surface, destroy_time, damage_time,
                         particle_spawners, hit_sound,
                         blood_on_kill, fade_out_step, screen_shake_on_kill)

    def target_collision(self):
        player = self.group_manager.player
        collision = player.hitbox.colliderect(self.hitbox)
        if collision and player.vulnerable:
            # dar o dano no player
            player.damage(self.damage)
            if self.hit_sound:
                self.hit_sound.play()

            # destruir o ataque
            self.kill()