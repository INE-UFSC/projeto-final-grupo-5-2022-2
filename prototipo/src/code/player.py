import math

import pygame

from damage_area import EnemyDamageArea
from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, attack_groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

        # ataques
        self.attack_groups = attack_groups
        # ataque básico
        self.attack_cooldown = 900
        self.can_attack = True
        self.attack_time = 0

        # cajado
        self.staff = Staff(groups, self)

    def create_attack(self):
        pos = (self.staff.rect.x, self.staff.rect.y + 15)
        sprite = pygame.image.load('../graphics/test/fireball.png').convert_alpha()
        # calcular direção do projétil
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[1] - mouse_pos[1], pos[0] - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # criar o projétil
        EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, speed=40, direction=direction, surface=sprite)

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # movimento vertical
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # movimento horizontal
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # ataque
        if mouse[0] and self.can_attack:
            self.create_attack()
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True

    def update(self):
        self.input()
        self.move(self.speed)
        self.cooldowns()


class Staff(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.image = pygame.image.load('../graphics/test/staff.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=self.player.rect.center)
        self.original_rect = self.rect

    def update(self):
        self.rect.center = self.player.rect.center + pygame.math.Vector2(25, 10)
        # atualizar posição do cajado
        mouse_pos = pygame.mouse.get_pos()
        dist = math.sqrt(
            (mouse_pos[0] - self.player.rect.centerx) ** 2 + (mouse_pos[1] - self.player.rect.centery) ** 2)
        angle = math.atan2(self.player.rect.centery - mouse_pos[1], self.player.rect.centerx - mouse_pos[0])
        sin = -math.sin(angle)
        cos = -math.cos(angle)
        offset = (dist // 32) ** 1 / 2
        self.rect.center = self.original_rect.center + pygame.Vector2(cos * offset, sin * offset)
