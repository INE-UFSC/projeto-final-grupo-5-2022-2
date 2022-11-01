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

        self.__health = 3
        self.__speed = 5

        self.__exp = 0
        self.__level_up_exp = 10
        self.__level_up_exp_increment = 10
        self.__current_level = 0
        self.__upgrade_points = 0

        self.obstacle_sprites = obstacle_sprites

        # ataques
        self.__attacks = [FireballAttack(attack_groups, obstacle_sprites),
                          SliceAttack(attack_groups, obstacle_sprites),
                          LineAttack(attack_groups, obstacle_sprites)]

        # dano
        self.__vulnerable = True
        self.__hurt_time = None
        self.__invincibility_duration = 500

        # cajado (somente desenha o sprite)
        self.__staff = Staff(groups)

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # movimento vertical
        if keys[pygame.K_w]:
            self._direction.y = -1
        elif keys[pygame.K_s]:
            self._direction.y = 1
        else:
            self._direction.y = 0
        # movimento horizontal
        if keys[pygame.K_d]:
            self._direction.x = 1
        elif keys[pygame.K_a]:
            self._direction.x = -1
        else:
            self._direction.x = 0

        # ataque
        if keys[pygame.K_q]:
            self.__attacks[2].use(self)

        if mouse[0]:
            self.__attacks[0].use(self)
        if mouse[2]:
            self.__attacks[1].use(self)

    def cooldowns(self):
        for attack in self.__attacks:
            attack.check_cooldown()

        if not self.__vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.__hurt_time >= self.__invincibility_duration:
                self.__vulnerable = True

    def animate(self):
        if not self.__vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def damage(self, damage):
        if self.__vulnerable:
            self.__health -= damage
            self.__vulnerable = False
            self.__hurt_time = pygame.time.get_ticks()

    def give_exp(self, exp):
        self.__exp += exp
        while self.__exp >= self.__level_up_exp:
            self.__exp -= self.__level_up_exp
            self.__current_level += 1
            self.__upgrade_points += 1
            self.__level_up_exp += self.__level_up_exp_increment

    def update(self):
        self.input()
        self.animate()
        self.staff.animate(self)
        self.move(self.__speed)
        self.cooldowns()

    @property
    def attacks(self):
        return self.__attacks

    @property
    def health(self):
        return self.__health

    @property
    def exp(self):
        return self.__exp

    @property
    def vulnerable(self):
        return self.__vulnerable

    @property
    def staff(self):
        return self.__staff


class Staff(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.__sprite_type = 'player'
        self.image = load_sprite('/test/staff.png')
        self.rect = self.image.get_rect()
        self.__original_rect = self.rect

    @property
    def sprite_type(self):
        return self.__sprite_type

    def animate(self, player):
        self.rect.center = player.rect.center + pygame.math.Vector2(25, 10)
        # atualizar posição do cajado
        mouse_pos = pygame.mouse.get_pos()
        dist = math.sqrt(
            (mouse_pos[0] - player.rect.centerx) ** 2 + (mouse_pos[1] - player.rect.centery) ** 2)
        angle = math.atan2(player.rect.centery - mouse_pos[1], player.rect.centerx - mouse_pos[0])
        sin = -math.sin(angle)
        cos = -math.cos(angle)
        offset = (dist // 32) ** 1 / 2
        self.rect.center = self.__original_rect.center + pygame.Vector2(cos * offset, sin * offset)
