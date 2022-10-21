import math

import pygame

from attack import FireballAttack
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
        self.attacks = {'fireball': FireballAttack(self, attack_groups, obstacle_sprites)}

        # cajado (somente o sprite)
        self.staff = Staff(groups, self)

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
        if mouse[0]:
            self.attacks['fireball'].use()

    def cooldowns(self):
        for attack in self.attacks:
            self.attacks[attack].check_cooldown()

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
