import math

import pygame

from code.level.GroupManager import GroupManager
from code.library.Resources import Resources
from code.level.particles.LightSource import LightSource


class Staff(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.__sprite_type = 'staff'
        self.__group_manager = GroupManager()
        self.__animation = Resources().get_animation('/staff')
        self.__frame_index = 0
        self.__animation_speed = 0.2
        self.__animate = False
        self.image = self.__animation[0]
        self.rect = self.image.get_rect()
        self.__original_rect = self.rect
        self.__light = None

    @property
    def sprite_type(self):
        return self.__sprite_type

    def toggle_animation(self):
        self.__animate = True
        # partícula de luz
        if self.__light:
            self.__light.kill()
        self.__light = LightSource(self.rect.center)
        self.__group_manager.add_to_particles(self.__light)

    def animate(self, player):
        if self.__animate:
            self.__light.rect.center = self.rect.center
            self.__frame_index += self.__animation_speed
            if self.__frame_index >= len(self.__animation):
                self.__frame_index = 0
                self.__animate = False
                self.__light.kill()
        else:
            self.__frame_index = 1 - self.__animation_speed
        self.image = self.__animation[int(self.__frame_index)]
        self.rect.center = player.rect.center + pygame.math.Vector2(20, -10)
        # atualizar posição do cajado
        mouse_pos = pygame.mouse.get_pos()
        dist = math.sqrt(
            (mouse_pos[0] - player.rect.centerx) ** 2 + (mouse_pos[1] - player.rect.centery) ** 2)
        angle = math.atan2(player.rect.centery - mouse_pos[1], player.rect.centerx - mouse_pos[0])
        sin = -math.sin(angle)
        cos = -math.cos(angle)
        offset = (dist // 32) ** 1 / 2
        self.rect.center = self.__original_rect.center + pygame.Vector2(cos * offset, sin * offset)
