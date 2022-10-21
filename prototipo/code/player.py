import math

import pygame

from attack import FireballAttack, LineAttack
from entity import Entity
from utils import load_sprite


class Player(Entity):
    def __init__(self, pos, groups, attack_groups, obstacle_sprites):
        super().__init__(groups)
        self.image = load_sprite('/test/player.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.health = 3
        self.exp = 0
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

        # ataques
        self.selected_attack = 1
        self.attacks = [FireballAttack(attack_groups, obstacle_sprites),
                        LineAttack(attack_groups, obstacle_sprites)]

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
        if keys[pygame.K_1] and len(self.attacks) >= 1:
            self.selected_attack = 1
        elif keys[pygame.K_2] and len(self.attacks) >= 2:
            self.selected_attack = 2

        if mouse[0]:
            if self.attacks[self.selected_attack - 1].can_attack:
                self.attacks[self.selected_attack - 1].use(self)

                if self.selected_attack != 1:
                    self.attacks[0].block()  # para o jogador não atirar uma bola de fogo imediatamente após um especial

            self.selected_attack = 1  # retornar após qualquer ataque para o básico

    def cooldowns(self):
        for attack in self.attacks:
            attack.check_cooldown()

    def update(self):
        self.input()
        self.move(self.speed)
        self.cooldowns()


class Staff(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.player = player
        self.image = load_sprite('/test/staff.png')
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
