import math

import pygame

from attack import FireballAttack, LineAttack, SliceAttack
from entity import Entity
from utils import load_sprite


class Player(Entity):
    def __init__(self, pos, groups, attack_groups, obstacle_sprites):
        super().__init__(groups, 'player')
        self.image = load_sprite('/test/player.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.health = 3
        self.exp = 0
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

        # ataques
        self.attacks = [FireballAttack(attack_groups, obstacle_sprites),
                        SliceAttack(attack_groups, obstacle_sprites),
                        LineAttack(attack_groups, obstacle_sprites)]

        # dano
        self.vulnerable = True
        self.hurt_time = None
        self.invincibility_duration = 500

        # cajado (somente desenha o sprite)
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
        if keys[pygame.K_q]:
            self.attacks[2].use(self)

        if mouse[0]:
            self.attacks[0].use(self)
        if mouse[2]:
            self.attacks[1].use(self)

    def cooldowns(self):
        for attack in self.attacks:
            attack.check_cooldown()

        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibility_duration:
                self.vulnerable = True

    def animate(self):
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def damage(self, damage):
        if self.vulnerable:
            self.health -= damage
            self.vulnerable = False
            self.hurt_time = pygame.time.get_ticks()

    def update(self):
        self.input()
        self.animate()
        self.move(self.speed)
        self.cooldowns()


class Staff(pygame.sprite.Sprite):
    def __init__(self, groups, player):
        super().__init__(groups)
        self.sprite_type = 'player'
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
