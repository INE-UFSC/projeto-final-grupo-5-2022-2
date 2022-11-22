import pygame

from code.group_manager import GroupManager
from code.wave_manager import WaveManager
from code.settings import *
from code.player import Player
from code.tile import Tile
from code.enemy import Enemy
from code.ui import UI

class Room:
    def __init__(self, room_map, player):
        # sprites
        self.__group_manager = GroupManager()
        # mapa
        self.__room_map = room_map
        # waves
        self.__wave_manager = WaveManager('1')
        # ui
        self.ui = UI()
        # player
        self.__player = player

    @property
    def player(self):
        return self.__player

    def create_map(self):
        for row_index, row in enumerate(self.__room_map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.__group_manager.visible_sprites, self.__group_manager.obstacle_sprites])
                elif col == 'p':
                    self.__player = Player([self.__group_manager.visible_sprites], [self.__group_manager.visible_sprites, self.__group_manager.attack_sprites],
                                         self.__group_manager.obstacle_sprites)
                elif col == 'e':
                    self.spawn_enemy('enemy', (x, y))

                elif col == 'p':
                    self.__player = Player((x, y), )
                elif col == 'e':
                    self.spawn_enemy('enemy', (x, y))

    def spawn_enemy(self, name, pos):
        Enemy(name, pos, [self.__group_manager.visible_sprites, self.__group_manager.attackable_sprites], self.__group_manager.obstacle_sprites)
        # permite os inimigos colidirem com os outros inimigos e com o player
        enemy_obstacle_sprites = pygame.sprite.Group(self.__player, self.__group_manager.obstacle_sprites, self.__group_manager.attackable_sprites)
        for sprite in self.__group_manager.attackable_sprites:
            sprite.obstacle_sprites = enemy_obstacle_sprites
        # permite o player colidir com os inimigos
        self.__player.obstacle_sprites = pygame.sprite.Group(self.__group_manager.obstacle_sprites, self.__group_manager.attackable_sprites)

    def toggle_menu(self):
        self.ui.toggle_menu()

    def run(self):
        self.__group_manager.visible_sprites.custom_draw()
        self.ui.display(self.__player, self.__wave_manager.timer)

        if not self.ui.is_menu_open:
            self.__wave_manager.update(self.spawn_enemy)
            self.__group_manager.visible_sprites.update()
            self.__group_manager.visible_sprites.enemy_update(self.__player)
            # conferir colisão dos ataques com os inimigos
            for attack_sprite in self.__group_manager.attack_sprites:
                attack_sprite.enemy_collision(self.__player, self.__group_manager.attackable_sprites)
