from abc import ABC, abstractmethod

from code.level.GroupManager import GroupManager
from code.library.Resources import Resources


class Attack(ABC):
    def __init__(self, icon, damage=1, cooldown=0, cast_sound='', hit_sound=''):
        self.__group_manager = GroupManager()
        self.__icon = Resources().get_sprite(icon)

        self.__base_damage = damage
        self.__damage = damage

        self.__base_cooldown = cooldown
        self.__cooldown = cooldown
        self.__can_attack = True
        self.__attack_time = 0

        if cast_sound != '':
            self.__cast_sound = Resources().get_sound(cast_sound)
        if hit_sound != '':
            self.__hit_sound = Resources().get_sound(hit_sound)

        self.block()  # iniciar com os ataques bloqueados

    def use(self, key):
        if self.__can_attack and key:
            GroupManager().player.staff.toggle_animation()
            self.create()
            self.block()

    def block(self):
        self.__can_attack = False
        self.__attack_time = self.__cooldown

    def check_cooldown(self):
        if not self.__can_attack:
            self.__attack_time -= 1
            if self.__attack_time <= 0:
                self.__can_attack = True

    @abstractmethod
    def create(self):
        pass

    @property
    def group_manager(self):
        return self.__group_manager

    @property
    def icon(self):
        return self.__icon

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, damage):
        self.__damage = damage

    @property
    def base_damage(self):
        return self.__base_damage

    @property
    def can_attack(self):
        return self.__can_attack

    @property
    def attack_time(self):
        return self.__attack_time

    @property
    def cooldown(self):
        return self.__cooldown

    @cooldown.setter
    def cooldown(self, cooldown):
        self.__cooldown = cooldown

    @property
    def base_cooldown(self):
        return self.__base_cooldown

    @property
    def cast_sound(self):
        return self.__cast_sound

    @property
    def hit_sound(self):
        return self.__hit_sound
