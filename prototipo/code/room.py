import pygame

from code.enemy import Enemy
from code.group_manager import GroupManager
from code.player import Player
from code.resources import Resources
from code.settings import *
from code.tile import Tile
from code.ui import UI
from code.wave_manager import WaveManager


class Room:
    def __init__(self, room_name):
        self.__ui = UI()
        self.__group_manager = GroupManager()
        self.__wave_manager = WaveManager()
        self.change_to(room_name)

    def change_to(self, room_name):
        self.__group_manager.clear_all_groups()
        self.__wave_manager.change_to_wave(room_name)
        self.create_map(room_name)

    @property
    def player(self):
        return self.__player

    def create_map(self, room_name):
        self.__group_manager.visible_sprites.set_background(room_name)

        if not hasattr(self, 'player'):
            self.__player = Player([self.__group_manager.visible_sprites],
                                   [self.__group_manager.visible_sprites, self.__group_manager.attack_sprites],
                                   self.__group_manager.obstacle_sprites)
        else:
            self.__group_manager.visible_sprites.add(self.__player)
            self.__group_manager.visible_sprites.add(self.__player.staff)

        # reposiciona o player
        self.__player.position = (TILESIZE, self.__player.position[1])

        # parede invisível ao redor da sala
        for i in range(0, WIDTH, TILESIZE):  # horizontal
            Tile((i, -TILESIZE), [self.__group_manager.obstacle_sprites], '')
            Tile((i, HEIGHT), [self.__group_manager.obstacle_sprites], '')
        for i in range(0, HEIGHT - TILESIZE, TILESIZE):  # vertical
            Tile((-TILESIZE, i), [self.__group_manager.obstacle_sprites], '')
            Tile((WIDTH, i), [self.__group_manager.obstacle_sprites], '')
        # tiles
        tiles = Resources().get_tilemap(room_name)
        for row_index, row in enumerate(tiles):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != '-1':
                    Tile((x, y), [self.__group_manager.visible_sprites, self.__group_manager.obstacle_sprites], col)

    def spawn_enemy(self, name, pos):
        Enemy(name, pos, [self.__group_manager.visible_sprites, self.__group_manager.attackable_sprites],
              self.__group_manager.obstacle_sprites)
        # permite os inimigos colidirem com os outros inimigos e com o player
        enemy_obstacle_sprites = pygame.sprite.Group(self.__player, self.__group_manager.obstacle_sprites,
                                                     self.__group_manager.attackable_sprites)
        for sprite in self.__group_manager.attackable_sprites:
            sprite.obstacle_sprites = enemy_obstacle_sprites
        # permite o player colidir com os inimigos
        self.__player.obstacle_sprites = pygame.sprite.Group(self.__group_manager.obstacle_sprites,
                                                             self.__group_manager.attackable_sprites)

    def toggle_menu(self):
        self.__ui.toggle_menu()

    def run(self):
        self.__group_manager.visible_sprites.custom_draw()
        self.__ui.display(self.__player, self.__wave_manager.timer)

        if not self.__ui.is_menu_open:
            self.__wave_manager.update(self.spawn_enemy)
            self.__group_manager.visible_sprites.update()
            self.__group_manager.visible_sprites.enemy_update(self.__player)
            # conferir colisão dos ataques com os inimigos
            for attack_sprite in self.__group_manager.attack_sprites:
                attack_sprite.enemy_collision(self.__player, self.__group_manager.attackable_sprites)
