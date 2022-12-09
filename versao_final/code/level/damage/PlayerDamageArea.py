import pygame

from code.level.damage.DamageArea import DamageArea


class PlayerDamageArea(DamageArea):
    def __init__(self, pos, surface, damage=0, speed=0, direction=pygame.math.Vector2(),
                 destroy_time=60, damage_time=0, particle_spawners=[], destroy_on_impact=False,
                 hit_sound=None, blood_on_kill=False, fade_out_step=0, screen_shake_on_kill=False):

        super().__init__(pos, surface, damage, speed, direction, destroy_on_impact, destroy_time, damage_time,
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
