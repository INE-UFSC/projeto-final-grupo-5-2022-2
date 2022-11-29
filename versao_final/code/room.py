import pygame

from code.camera import Camera
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
        self.__camera = Camera()
        self.__group_manager = GroupManager()
        self.__wave_manager = WaveManager()
        self.change_to(room_name)

    def change_to(self, room_name):
        self.__group_manager.clear_all()
        self.__wave_manager.change_to_wave(room_name)
        self.create_map(room_name)

    @property
    def player(self):
        return self.__player

    def create_map(self, room_name):
        self.__camera.set_background(room_name)

        if not hasattr(self, 'player'):
            self.__player = Player()
        else:
            # TODO: posicionar o player
            pass

        # tiles
        tiles = Resources().get_tilemap(room_name)
        for row_index, row in enumerate(tiles):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != '-1':
                    Tile((x, y), col)

    def spawn_enemy(self, enemy_class, pos):
        enemy_class(pos)

    def toggle_menu(self):
        self.__ui.toggle_menu()

    def run(self):
        self.__camera.draw(self.__group_manager.visible_sprites)
        self.__ui.display(self.__player, self.__wave_manager.timer)

        if not self.__ui.is_menu_open:
            self.__wave_manager.update(self.spawn_enemy)
            self.__group_manager.visible_sprites.update()
            # conferir colisão dos ataques com os inimigos
            for attack_sprite in self.__group_manager.attack_sprites:
                attack_sprite.enemy_collision()
