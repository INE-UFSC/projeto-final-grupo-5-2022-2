import pygame

from code.settings import TILESIZE
from code.sprite_manager import SpriteManager


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__back_sprite_types = ['on_ground']
        self.__front_sprite_types = ['light']
        self.__background = pygame.Surface((TILESIZE, TILESIZE))

    def custom_draw(self):
        self.__display_surface.blit(self.__background, (0, 0))
        # separar os sprites que devem sempre ir atrás dos outros e sempre na frente
        # alguns sprites que necessariamente devem ir atrás são as partículas de sangue, que devem ficar
        # atrás de tudo por "estar no chão"
        # a maioria dos sprites fica no meio
        # um sprite que necessariamente deve ir na frente são as partículas de luz
        back_sprites = list(filter(
            lambda sprite: sprite.sprite_type in self.__back_sprite_types, self.sprites()))
        middle_sprites = list(
            filter(lambda sprite: sprite.sprite_type not in self.__back_sprite_types + self.__front_sprite_types,
                   self.sprites()))
        front_sprites = list(filter(
            lambda sprite: sprite.sprite_type in self.__front_sprite_types, self.sprites()))
        # desenhar os sprites na ordem
        sprite_lists = [back_sprites, middle_sprites, front_sprites]
        for sprite_list in sprite_lists:
            for sprite in sorted(sprite_list, key=lambda sprite: sprite.rect.centery):
                self.__display_surface.blit(sprite.image, sprite.rect)

    def enemy_update(self, player):
        # os inimigos possuem um update() chamado enemy_update() que precisa receber o player como
        # parâmetro para algumas interações
        # essa função chama esse outro update()
        enemy_sprites = [sprite for sprite in self.sprites()
                         if sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

    def set_background(self, room_name):
        self.__background = SpriteManager().get_sprite(f'/backgrounds/{room_name}.png')
