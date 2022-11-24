import pygame

from code.enemy import Enemy
from code.group_manager import GroupManager
from code.player import Player
from code.settings import *
from code.tile import Tile
from code.ui import UI
from code.utils import load_objects
from code.wave_manager import WaveManager


class Room:
    def __init__(self, room_name):
        self.__ui = UI()
        self.change_to(room_name)

    def change_to(self, room_name):
        self.__group_manager = GroupManager()
        self.__wave_manager = WaveManager(room_name)
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
        # else:
        # TODO: adicionar o jogador atual nos grupos da próxima sala

        # TODO: Fazer a parede que não deixa o player passar
        objects = load_objects(room_name)
        for row_index, row in enumerate(objects):
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
