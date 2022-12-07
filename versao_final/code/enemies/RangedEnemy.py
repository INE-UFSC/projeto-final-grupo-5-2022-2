from abc import ABC

import pygame

from code.Entity import Entity
from code.Resources import Resources
from code.damage.PlayerDamageArea import PlayerDamageArea
from code.enemies.BasicEnemy import Enemy
from code.enemies.EnemyStatus import RangedStatus


class RangedEnemy(Enemy, ABC):
    def __init__(self, name, pos, range, target_distance, projectile_damage,
                 projectile_speed, flee_distance, health, speed, collision_damage, exp,
                 attack_cooldown):
        super().__init__(name, pos, health, speed, collision_damage, exp,
                         attack_cooldown)
        self.__range = range
        self.__target_distance = target_distance
        self.__flee_distance = flee_distance
        self.__projectile_sprite = Resources().get_sprite(f'/enemies/{name}/projectile.png')
        self.__projectile_damage = projectile_damage
        self.__projectile_speed = projectile_speed
        self.__projectile_cooldown = attack_cooldown

        self.__status = RangedStatus.MOVE

        self.__is_attacking = False

    def update(self):
        self.distance = Entity.get_distance(self, self.group_manager.player)
        super().update()

    def get_status(self):
        # decide o status atual
        if self.group_manager.player.hitbox.colliderect(self.damage_hitbox) and self.can_attack:
            self.status = RangedStatus.MELEE
        elif self.status == RangedStatus.ATTACK:
            if self.distance > self.range:
                self.status = RangedStatus.MOVE
            elif self.distance < self.flee_distance:
                self.status = RangedStatus.FLEE
        elif self.distance < self.target_distance:
            self.status = RangedStatus.ATTACK
        else:
            self.status = RangedStatus.MOVE

    def actions(self):
        # sobrescreve o método actions da classe Enemy
        # muda os status possíveis do inimigo
        player = self.group_manager.player
        if self.status == RangedStatus.MELEE:
            self.attack_time = self.attack_cooldown
            self.can_attack = False  # TODO: passar para a lógica do animate() ao adicionar sprites
            player.damage(self.collision_damage)
        elif self.status == RangedStatus.MOVE:
            self.direction = self.get_player_distance_direction()[1]
        elif self.status == RangedStatus.FLEE:
            self.direction = -self.get_player_distance_direction()[1]
        else:
            if self.status == RangedStatus.ATTACK and self.projectile_cooldown <= 0 and not self.is_attacking:
                self.is_attacking = True
                self.animation = Resources().get_animation(f'/enemies/{self.name}/attack')
                self.frame_index = 0
            self.direction = pygame.math.Vector2()

    def animate(self):
        if self.is_attacking:
            if self.frame_index >= len(self.animation) - 1:
                self.is_attacking = False
                self.launch_projectile()
                self.animation = Resources().get_animation(f'/enemies/{self.name}/move')
        super().animate()

    def launch_projectile(self):
        self.projectile_cooldown = self.attack_cooldown
        projectile = PlayerDamageArea(self.position, self.projectile_damage, self.projectile_speed,
                                      self.get_player_distance_direction()[1],
                                      surface=self.projectile_sprite)
        self.group_manager.add_to_enemy_attacks(projectile)

    def cooldowns(self):
        super().cooldowns()
        self.projectile_cooldown -= 1

    @property
    def range(self):
        return self.__range

    @property
    def target_distance(self):
        return self.__target_distance

    @property
    def flee_distance(self):
        return self.__flee_distance

    @property
    def projectile_sprite(self):
        return self.__projectile_sprite

    @property
    def projectile_damage(self):
        return self.__projectile_damage

    @property
    def projectile_speed(self):
        return self.__projectile_speed

    @property
    def projectile_cooldown(self):
        return self.__projectile_cooldown

    @projectile_cooldown.setter
    def projectile_cooldown(self, value):
        self.__projectile_cooldown = value

    @property
    def is_attacking(self):
        return self.__is_attacking

    @is_attacking.setter
    def is_attacking(self, value):
        self.__is_attacking = value

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, value):
        self.__distance = value
