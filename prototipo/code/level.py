import pygame.math

from code.enemy import Enemy
from code.particles import *
from code.player import Player
from code.settings import *
from code.tile import Tile
from code.ui import UI
from code.waves import WaveManager
from code.y_sort_camera_group import YSortCameraGroup


class Level:
    def __init__(self):
        # salas
        self.__room_list = list([Room(ROOM_MAP_1), Room(ROOM_MAP_2)])
        self.__current_room_index = 0

    @property
    def current_room(self):
        return self.__room_list[self.__current_room_index]

    @current_room.setter
    def current_room(self, index):
        self.__current_room_index = index

    def toggle_menu(self):
        self.current_room.toggle_menu()

    def run(self):
        self.current_room.run()
        if self.current_room.player.rect.topleft[0] > WIDTH - 192:  # mudar
            self.__current_room_index += 1


class Room:
    def __init__(self, room_map):
        # sprites
        self.__visible_sprites = YSortCameraGroup()
        self.__obstacle_sprites = pygame.sprite.Group()
        self.__attack_sprites = pygame.sprite.Group()
        self.__attackable_sprites = pygame.sprite.Group()
        # mapa
        self.create_map(room_map)
        # waves
        self.__wave_manager = WaveManager('1')
        # ui
        self.__ui = UI()

    @property
    def visible_sprites(self):
        return self.__visible_sprites

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def attack_sprites(self):
        return self.__attack_sprites

    @property
    def attackable_sprites(self):
        return self.__attackable_sprites

    @property
    def wave_maneger(self):
        return self.__wave_manager

    @property
    def ui(self):
        return self.__ui

    @property
    def player(self):
        return self.__player

    def create_map(self, room_map):
        for row_index, row in enumerate(room_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.__player = Player([self.__visible_sprites],
                                           [self.__visible_sprites, self.__attack_sprites],
                                           self.__obstacle_sprites)
                elif col == 'e':
                    self.spawn_enemy('enemy', (x, y))

    def spawn_enemy(self, name, pos):
        Enemy(name, pos, [self.__visible_sprites, self.__attackable_sprites], self.obstacle_sprites)
        # permite os inimigos colidirem com os outros inimigos e com o player
        enemy_obstacle_sprites = pygame.sprite.Group(self.__player, self.__obstacle_sprites, self.__attackable_sprites)
        for sprite in self.attackable_sprites:
            sprite.obstacle_sprites = enemy_obstacle_sprites
        # permite o player colidir com os inimigos
        self.__player.obstacle_sprites = pygame.sprite.Group(self.__obstacle_sprites, self.__attackable_sprites)

    def toggle_menu(self):
        self.ui.toggle_menu()

    def run(self):
        self.visible_sprites.custom_draw()
        self.ui.display(self.__player, self.__wave_manager.timer)

        if not self.ui.is_menu_open:
            self.__wave_manager.update(self.spawn_enemy)
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.__player)
            # conferir colisão dos ataques com os inimigos
            for attack_sprite in self.attack_sprites:
                attack_sprite.enemy_collision(self.__player, self.attackable_sprites)
