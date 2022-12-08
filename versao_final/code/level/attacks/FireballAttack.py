import math

import pygame

from code.level.damage.EnemyDamageArea import EnemyDamageArea
from code.level.GroupManager import GroupManager
from code.library.Resources import Resources
from code.level.attacks.Attack import Attack
from code.level.particles.FireSource import FireSource
from code.level.particles.LightSource import LightSource


class FireballAttack(Attack):
    def __init__(self):
        super().__init__('/icons/fireball_attack.png', damage=1, cooldown=75, cast_sound='fireball_cast.ogg',
                         hit_sound='fireball_hit.ogg')
        self.cast_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.1)

    def create(self):
        player = GroupManager().player
        pos = (player.staff.rect.x, player.staff.rect.y)
        sprite = Resources().get_sprite('/attacks/fireball.png')
        # calcular direção do projétil
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[1] - mouse_pos[1], pos[0] - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # criar o projétil
        light = LightSource(pos)
        fire = FireSource(pos)
        self.group_manager.add_to_particles(light)
        self.group_manager.add_to_particles(fire)
        damage_area = EnemyDamageArea(pos, damage=self.damage, speed=40, direction=direction, destroy_on_impact=True,
                                      surface=sprite, particle_spawners=[light, fire], hit_sound=self.hit_sound)
        self.group_manager.add_to_attacks(damage_area)
        self.cast_sound.play()
