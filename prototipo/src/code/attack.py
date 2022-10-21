import math
from abc import ABC, abstractmethod

import pygame

from damage_area import EnemyDamageArea


class Attack(ABC):
    def __init__(self, player, attack_groups, obstacle_sprites, cooldown=0):
        self.player = player
        self.attack_groups = attack_groups
        self.obstacle_sprites = obstacle_sprites

        self.cooldown = cooldown
        self.can_attack = True
        self.attack_time = 0

    def use(self):
        if self.can_attack:
            self.create()
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()

    def check_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack and current_time - self.attack_time >= self.cooldown:
            self.can_attack = True

    @abstractmethod
    def create(self):
        pass


class FireballAttack(Attack):
    def __init__(self, attack_groups, player, obstacle_sprites):
        super().__init__(attack_groups, player, obstacle_sprites, cooldown=900)

    def create(self):
        pos = (self.player.staff.rect.x, self.player.staff.rect.y + 15)
        sprite = pygame.image.load('../graphics/test/fireball.png').convert_alpha()
        # calcular direção do projétil
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[1] - mouse_pos[1], pos[0] - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # criar o projétil
        EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, speed=40, direction=direction, surface=sprite)
