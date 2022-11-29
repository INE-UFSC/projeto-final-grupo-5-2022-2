import random

import pygame

from code.resources import Resources
from code.settings import TILESIZE
from code.singleton import Singleton


class Camera(Singleton):
    def __init__(self):
        if not self._initialized:
            self.__display_surface = pygame.display.get_surface()
            self.__back_sprite_types = ['on_ground']
            self.__front_sprite_types = ['light']
            self.__background = pygame.Surface((TILESIZE, TILESIZE))
            self.__background_shadow = Resources().get_sprite('/backgrounds/shadow_overlay.png')
            self.__screen_shake_offset = pygame.math.Vector2()
            self._initialized = True

    def set_background(self, room_name):
        self.__background = Resources().get_sprite(f'/backgrounds/{room_name}.png')

    def shake(self):
        self.__screen_shake_offset.x += random.randint(-16, 16)
        self.__screen_shake_offset.y += random.randint(-16, 16)

    def draw(self, sprites):
        # screen shake
        if self.__screen_shake_offset != pygame.math.Vector2():
            self.__screen_shake_offset *= 0.90
            if -1 <= self.__screen_shake_offset.magnitude() <= 1:
                self.__screen_shake_offset = pygame.math.Vector2()

        # fundo
        self.__display_surface.blit(self.__background, self.__screen_shake_offset)
        self.__display_surface.blit(self.__background_shadow, self.__screen_shake_offset)
        # separar os sprites que devem sempre ir atrás dos outros e sempre na frente
        # alguns sprites que necessariamente devem ir atrás são as partículas de sangue, que devem ficar
        # atrás de tudo por "estar no chão"
        # a maioria dos sprites fica no meio
        # um sprite que necessariamente deve ir na frente são as partículas de luz
        back_sprites = (sprite for sprite in sprites if sprite.sprite_type in self.__back_sprite_types)
        middle_sprites = (sprite for sprite in sprites if
                          sprite.sprite_type not in self.__back_sprite_types + self.__front_sprite_types)
        front_sprites = (sprite for sprite in sprites if sprite.sprite_type in self.__front_sprite_types)
        # desenhar os sprites na ordem
        sprite_lists = (back_sprites, middle_sprites, front_sprites)
        for sprite_list in sprite_lists:
            for sprite in sorted(sprite_list, key=lambda sprite: sprite.rect.bottom):
                self.__display_surface.blit(sprite.image, sprite.rect.topleft + self.__screen_shake_offset)
