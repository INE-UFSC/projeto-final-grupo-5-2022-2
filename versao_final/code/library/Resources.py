import json
import os
from code.library.Settings import Settings
from code.library.Singleton import Singleton
from csv import reader

import pygame


class Resources(Singleton):
    def __init__(self):
        if not self._initialized:
            self.__settings = Settings()
            self.__cache = {}
            self.__load_resources()
            self._initialized = True
            
    def __load_resources(self):
        extensions = {'.png': self.__load_image,
                      '.ogg': self.__load_sound,
                      '.csv': self.__load_tilemap,
                      '.json': self.__load_wave}
        for root, dirs, files in os.walk(self.__settings.GAME_PATH):
            for file in files:
                name, extension = os.path.splitext(file)
                if extension in extensions.keys():
                    full_path = os.path.join(root, file)
                    relative_path = '/' + os.path.relpath(full_path, self.__settings.GAME_PATH).replace('\\', '/')
                    self.__cache[relative_path] = extensions[extension](full_path)
        print(f'[{pygame.time.get_ticks()}] Recursos carregados')

    def __load_image(self, path):
        return pygame.image.load(path).convert_alpha()

    def __load_sound(self, path):
        return pygame.mixer.Sound(path)

    def __load_tilemap(self, path):
        tiles = list()
        with open(path) as csv_file:
            layout = reader(csv_file, delimiter=',')
            for row in layout:
                tiles.append(row)
            return tiles

    def __load_wave(self, path):
        with open(path, 'r', encoding='UTF-8') as file:
            return json.load(file)[0]

    def has_save(self) -> bool:
        return os.listdir(f'{self.__settings.SAVE_PATH}/{self.__settings.save_name}')
        try:
            with open(f'{self.__settings.SAVE_PATH}/{self.__settings.save_name}', 'r'):
                return True
        except FileNotFoundError:
            return False
        
    def get_sprite(self, file):
        file_dir = file.replace('\\', '/')
        return self.__cache[f'/graphics{file_dir}']

    def get_animation(self, folder_name):
        surface_list = []
        for _, __, img_files in os.walk(f'{self.__settings.GAME_PATH}/graphics/{folder_name}'):
            for image in img_files:
                image_surf = self.get_sprite(f'{folder_name}/{image}').copy()
                surface_list.append(image_surf)
        return surface_list

    def get_sound(self, file):
        file_dir = file.replace('\\', '/')
        return self.__cache[f'/audio/{file_dir}']

    def get_tilemap(self, room_name):
        return self.__cache[f'/rooms/{room_name}/tiles.csv']

    def get_wave(self, room_name):
        return self.__cache[f'/rooms/{room_name}/wave.json']
