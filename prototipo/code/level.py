import pygame.math

from enemy import Enemy
from particles import *
from player import Player
from settings import *
from tile import Tile
from ui import UI


class Level:
    def __init__(self):
        self.__display_surface = pygame.display.get_surface()

        # criar o mapa
        self.__rooms_list = list()
        self.__rooms_list.append(Room(WORLD_MAP))
        self.__current_room = self.__rooms_list[0]

        self.ui = UI()

        self.timer = 0  # TEMPORÁRIO

    @property
    def visible_sprites(self):
        return self.current_room.visible_sprites

    @property
    def obstacle_sprites(self):
        return self.current_room.obstacle_sprites

    @property
    def attack_sprites(self):
        return self.current_room.attack_sprites

    @property
    def attackable_sprites(self):
        return self.current_room.attackable_sprites

    @property
    def rooms_list(self):
        return self.__rooms_list

    @property
    def current_room(self):
        return self.__current_room

    @current_room.setter
    def current_room(self, room):
        self.__current_room = room

    def spawn_enemy(self, pos):
        e = Enemy('test', pos, [self.current_room.visible_sprites,
                  self.current_room.attackable_sprites], self.obstacle_sprites)

        # permite os inimigos colidirem com os outros inimigos e com o player
        enemy_obstacle_sprites = pygame.sprite.Group(
            self.current_room.player, self.obstacle_sprites, self.attackable_sprites)
        for sprite in self.attackable_sprites:
            sprite.obstacle_sprites = enemy_obstacle_sprites
        # permite o player colidir com os inimigos
        self.current_room.player.obstacle_sprites = pygame.sprite.Group(
            self.obstacle_sprites, self.attackable_sprites)

    def run(self):
        self.current_room.visible_sprites.custom_draw()
        self.current_room.visible_sprites.update()
        self.current_room.visible_sprites.enemy_update(
            self.current_room.player)

        # conferir colisão dos ataques com os inimigos
        for attack_sprite in self.current_room.attack_sprites:
            attack_sprite.enemy_collision(
                self.current_room.player, self.current_room.attackable_sprites)

        self.ui.display(self.current_room.player)

        # invocar inimigo (TEMPORÁRIO)
        self.timer += 1
        if self.timer % 120 == 0:
            self.spawn_enemy((320, 320))


class Room:
    def __init__(self, room_map):
        # sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # mapa
        self.__room_map = room_map

        self.create_map()

    @property
    def room_map(self):
        return self.__room_map

    def create_map(self):
        for row_index, row in enumerate(self.room_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], [self.visible_sprites, self.attack_sprites],
                                         self.obstacle_sprites)
                elif col == 'e':
                    Enemy('test', (x, y), [
                          self.visible_sprites, self.attackable_sprites], self.obstacle_sprites)

        # permite os inimigos colidirem com os outros inimigos e com o player
        enemy_obstacle_sprites = pygame.sprite.Group(
            self.player, self.obstacle_sprites, self.attackable_sprites)
        for sprite in self.attackable_sprites:
            sprite.obstacle_sprites = enemy_obstacle_sprites
        # permite o player colidir com os inimigos
        self.player.obstacle_sprites = pygame.sprite.Group(
            self.obstacle_sprites, self.attackable_sprites)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__back_sprite_types = ['on_ground']
        self.__front_sprite_types = ['light']

    def custom_draw(self):
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
