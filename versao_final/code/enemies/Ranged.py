import pygame

from code.enemies.Enemy import Enemy
from code.enemies.PlayerDamageArea import PlayerDamageArea
from code.Entity import Entity
from code.Resources import Resources


class Ranged(Enemy):
    def __init__(self, name, pos, range, target_distance, projectile_sprite, projectile_damage,
                 projectile_speed, flee_distance, health, speed, collision_damage, exp,
                 attack_cooldown):
        super().__init__(name, pos, health, speed, collision_damage, exp,
                         attack_cooldown)
        self.__range = range
        self.__target_distance = target_distance
        self.__flee_distance = flee_distance
        self.__projectile_sprite = Resources().get_sprite(projectile_sprite)
        self.__projectile_damage = projectile_damage
        self.__projectile_speed = projectile_speed
        self.__projectile_cooldown = attack_cooldown

        self.__in_range = False

    def update(self):
        self.distance = Entity.get_distance(self, self._group_manager.player)
        super().update()

    def get_status(self):
        # decide o status atual
        if self._group_manager.player.hitbox.colliderect(self.damage_hitbox) and self.can_attack:
            self.status = 'melee'
        elif self.status == 'attack':
            self.in_range = True
            if self.distance > self.range:
                self.status = 'move'
                self.in_range = False
            elif self.distance < self.flee_distance:
                self.status = 'flee'
        elif self.distance < self.target_distance:
            self.status = 'attack'
            self.in_range = True
        else:
            self.status = 'move'
            self.in_range = False

    def actions(self):
        # sobrescreve o método actions da classe Enemy
        # muda os status possíveis do inimigo
        player = self._group_manager.player
        if self.status == 'melee':
            self.attack_time = self.attack_cooldown
            self.can_attack = False  # TODO: passar para a lógica do animate() ao adicionar sprites
            player.damage(self.collision_damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction()[1]
        elif self.status == 'flee':
            self.direction = -self.get_player_distance_direction()[1]
        else:
            self.direction = pygame.math.Vector2()

        # sempre ataca a distância se estiver no alcance
        if self.projectile_cooldown < 0 and self.in_range:
            self.projectile_cooldown = self.attack_cooldown
            projectile = PlayerDamageArea(self.position, self.projectile_damage, self.projectile_speed,
                                          self.get_player_distance_direction()[1], self.projectile_sprite)
            self._group_manager.add_to_enemy_attacks(projectile)

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
    def in_range(self):
        return self.__in_range
    
    @in_range.setter
    def in_range(self, value):
        self.__in_range = value

    @property
    def distance(self):
        return self.__distance

    @distance.setter
    def distance(self, value):
        self.__distance = value