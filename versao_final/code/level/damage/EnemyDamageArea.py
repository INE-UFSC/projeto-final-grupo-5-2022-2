import pygame

from code.level.Camera import Camera
from code.library.Settings import TILESIZE
from code.level.damage.DamageArea import DamageArea
from code.level.particles.BloodSource import BloodSource


class EnemyDamageArea(DamageArea):
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
        if not self.damage_time > 0:
            # dar dano somente enquanto o damage time for maior que 0
            return

        collision_sprites = pygame.sprite.spritecollide(self, self.group_manager.enemy_sprites, False)
        if collision_sprites:
            for target_sprite in collision_sprites:
                if not target_sprite.vulnerable:  # pular os inimigos que não estão vulneráveis
                    continue

                if self.hit_sound:
                    self.hit_sound.play()

                target_sprite.damage(self.damage)
                if target_sprite.health <= 0:
                    target_sprite.check_death()

                    if self.blood_on_kill:
                        blood = BloodSource(collision_sprites[0].rect.center, self.direction)
                        self.group_manager.add_to_particles(blood)
                    if self.screen_shake_on_kill:
                        Camera().shake()

                if self.destroy_on_impact:  # ataque dá dano em só um inimigo
                    self.kill()
                    break
