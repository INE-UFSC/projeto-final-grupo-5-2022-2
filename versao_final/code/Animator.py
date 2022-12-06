import math
from code.GroupManager import GroupManager
from code.Resources import Resources

import pygame


class Animator:
    def __init__(self, animations_path : str, animations : tuple) -> None:
        self.__animations = dict
        for animation in animations:
            self.__animations[animation] = Resources.get_animation(f'{animations_path}/{animation}')
        self.__group_manager = GroupManager()

        self.blink = False

    def tick(self, animation) -> bool:
        self.__frame_index += self.animation_speed
        
        # animação de vulnerabilidade
        if not self.blink:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        # returna True se está no último frame da animação
        if self.__frame_index >= len(self.animations[animation]):
            self.__frame_index = 0
            return True
        return False

    def wave_value():
        # utilizado como o alpha do efeito de flickering (piscando) quando a entidade recebe dano
        value = math.sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    @property
    def animations(self) -> dict:
        return self.__animations

    @property
    def blink(self) -> bool:
        return self.blink

    @blink.setter
    def blink(self, value : bool) -> None:
        self.blink = value