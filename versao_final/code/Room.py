from code.Camera import Camera
from code.GroupManager import GroupManager
from code.Player import Player
from code.Resources import Resources
from code.Settings import *
from code.Tile import Tile
from code.ui.UI import UI
from code.WaveManager import WaveManager


class Room:
    def __init__(self, room_name):
        self.__ui = UI()
        self.__camera = Camera()
        self.__group_manager = GroupManager()
        self.__wave_manager = WaveManager()
        self.tiles = []
        self.change_to(room_name)

    def change_to(self, room_name):
        self.__group_manager.clear_all()
        self.__wave_manager.change_to_wave(room_name)
        self.create_map(room_name)

    def create_map(self, room_name):
        self.__camera.set_background(room_name)

        if self.__group_manager.player is None:
            self.__player = Player()
        else:
            self.__player.position = (TILESIZE, self.__player.position[1])

        # tiles
        self.tiles = Resources().get_tilemap(room_name)
        for row_index, row in enumerate(self.tiles):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col != '-1':
                    Tile((x, y), col)

    def toggle_menu(self):
        self.__ui.toggle_menu()

    def room_ended(self):
        return self.__wave_manager.wave_ended() and len(self.__group_manager.enemy_sprites) == 0

    def run(self):
        self.__camera.draw(self.__group_manager.visible_sprites)
        self.__ui.display(self.__group_manager.player, self.__wave_manager.timer)

        if not self.__ui.is_menu_open():
            self.__wave_manager.update()
            self.__group_manager.visible_sprites.update()

    @property
    def tiles(self):
        return self.__tiles

    @tiles.setter
    def tiles(self, tiles):
        self.__tiles = tiles