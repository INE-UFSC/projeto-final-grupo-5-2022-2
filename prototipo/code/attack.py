import math
from abc import ABC, abstractmethod

import pygame

from damage_area import EnemyDamageArea
from utils import load_sprite


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
            self.block()

    def block(self):
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
        pos = (self.player.staff.rect.x, self.player.staff.rect.y)
        sprite = load_sprite('/test/fireball.png')
        # calcular direção do projétil
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[1] - mouse_pos[1], pos[0] - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # criar o projétil
        EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, speed=40, direction=direction, surface=sprite)


class LineAttack(Attack):
    def __init__(self, attack_groups, player, obstacle_sprites):
        super().__init__(attack_groups, player, obstacle_sprites, cooldown=2400)

    def create(self):
        pos = (self.player.staff.rect.centerx, self.player.staff.rect.y + 12)
        sprite = load_sprite('/test/kamehameha.png')
        pivot = (0, 12)
        # rotacionar o sprite
        mouse_pos = pygame.mouse.get_pos()
        angle = 360 - math.degrees(math.atan2(mouse_pos[1] - pos[1], mouse_pos[0] - pos[0]))
        image_rect = sprite.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        sprite = pygame.transform.rotate(sprite, angle)
        sprite_rect = sprite.get_rect(center=rotated_image_center)
        # criar o ataque
        damage_area = EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, surface=sprite, destroy_time=180)
        damage_area.rect = sprite_rect
