from code.level.Camera import Camera
from code.level.GroupManager import GroupManager
from code.level.Player import Player
from code.level.Tile import Tile
from code.level.WaveManager import WaveManager
from code.library.Resources import Resources
from code.library.Settings import Settings
from code.ui.LevelUI import UI


class Room:
    def __init__(self, room_name):
        self.__settings = Settings()
        self.__ui = UI()
        self.__camera = Camera()
        self.__group_manager = GroupManager()
        self.__wave_manager = WaveManager()
        self.tiles = []
        self.change_to(room_name)

        # para a lógica de out of bounds
        player = self.__group_manager.player
        self.__min_x = -player.image.get_width()
        self.__min_y = -player.image.get_height()
        self.__width = self.__settings.WIDTH
        self.__height = self.__settings.HEIGHT
        self.__coordinates = {'top': (self.__width // 2, self.__min_y), 'bottom': (self.__width // 2, self.__height),
                              'left': (self.__min_x, self.__height // 2), 'right': (self.__width, self.__height // 2)}

    def change_to(self, room_name):
        self.__group_manager.clear_all()
        self.__wave_manager.change_to_wave(room_name)
        self.create_map(room_name)

    def create_map(self, room_name):
        self.__camera.set_background(room_name)

        if self.__group_manager.player is None:
            player = Player()
            self.__group_manager.player = player
        else:
            # TODO: arrumar isso
            player = self.__group_manager.player
            player.position = (self.__settings.TILESIZE, player.position[1])

        # tiles
        self.tiles = Resources().get_tilemap(room_name)
        for row_index, row in enumerate(self.tiles):
            for col_index, col in enumerate(row):
                x = col_index * self.__settings.TILESIZE
                y = row_index * self.__settings.TILESIZE
                if col != '-1':
                    tile = Tile((x, y), col)
                    self.__group_manager.add_to_tiles(tile)

    def toggle_menu(self):
        self.__ui.toggle_menu()

    @property
    def room_ended(self):
        return self.__wave_manager.wave_ended and len(self.__group_manager.enemy_sprites) == 0

    @property
    def exit_clicked(self):
        return self.__ui.exit_clicked

    def __check_player_out_of_bounds(self):
        player = self.__group_manager.player
        if player.hitbox.x < self.__min_x:
            player.hitbox.topleft = self.__coordinates['right']
        elif player.hitbox.x > self.__width:
            player.hitbox.topleft = self.__coordinates['left']
        if player.hitbox.y < self.__min_y:
            player.hitbox.topleft = self.__coordinates['bottom']
        elif player.hitbox.y > self.__height:
            player.hitbox.topleft = self.__coordinates['top']

    @property
    def is_player_dead(self):
        return self.__group_manager.player.is_dead

    def run(self):
        self.__camera.draw(self.__group_manager.visible_sprites)
        self.__ui.display(self.__group_manager.player, self.__wave_manager.timer)

        if not self.__ui.is_menu_open:
            self.__check_player_out_of_bounds()
            self.__wave_manager.update()
            self.__group_manager.visible_sprites.update()

    @property
    def tiles(self):
        return self.__tiles

    @tiles.setter
    def tiles(self, tiles):
        self.__tiles = tiles
