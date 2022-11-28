import random

import pygame

from code.resources import Resources
from code.settings import TILESIZE


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__back_sprite_types = ['on_ground']
        self.__front_sprite_types = ['light', 'staff']
        self.__background = pygame.Surface((TILESIZE, TILESIZE))
        self.__background_shadow = Resources().get_sprite('/backgrounds/shadow_overlay.png')
        self.__screen_shake = pygame.math.Vector2()

    def shake(self):
        self.__screen_shake.x += random.randint(-16, 16)
        self.__screen_shake.y += random.randint(-16, 16)

    def custom_draw(self):
        # screen shake
        if self.__screen_shake != pygame.math.Vector2():
            self.__screen_shake *= 0.90
            if -1 <= self.__screen_shake.magnitude() <= 1:
                self.__screen_shake = pygame.math.Vector2()

        # fundo
        self.__display_surface.blit(self.__background, self.__screen_shake)
        self.__display_surface.blit(self.__background_shadow, self.__screen_shake)
        # separar os sprites que devem sempre ir atrás dos outros e sempre na frente
        # alguns sprites que necessariamente devem ir atrás são as partículas de sangue, que devem ficar
        # atrás de tudo por "estar no chão"
        # a maioria dos sprites fica no meio
        # um sprite que necessariamente deve ir na frente são as partículas de luz
        back_sprites = (sprite for sprite in self.sprites() if sprite.sprite_type in self.__back_sprite_types)
        middle_sprites = (sprite for sprite in self.sprites() if
                          sprite.sprite_type not in self.__back_sprite_types + self.__front_sprite_types)
        front_sprites = (sprite for sprite in self.sprites() if sprite.sprite_type in self.__front_sprite_types)
        # desenhar os sprites na ordem
        sprite_lists = (back_sprites, middle_sprites, front_sprites)
        for sprite_list in sprite_lists:
            for sprite in sorted(sprite_list, key=lambda sprite: sprite.rect.centery):
                self.__display_surface.blit(sprite.image, sprite.rect.topleft + self.__screen_shake)

    def enemy_update(self, player):
        # os inimigos possuem um update() chamado enemy_update() que precisa receber o player como
        # parâmetro para algumas interações
        # essa função chama esse outro update()
        enemy_sprites = [sprite for sprite in self.sprites()
                         if sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def set_background(self, room_name):
        self.__background = Resources().get_sprite(f'/backgrounds/{room_name}.png')
