import os

import pygame

from code.settings import GAME_PATH
from code.singleton import Singleton


class SpriteManager(Singleton):
    def __init__(self):
        if not self._initialized:
            self.__cache = {}
            self.__load_all_sprites()
            self._initialized = True

    def __load_all_sprites(self):
        graphics_path = os.path.join(GAME_PATH, 'graphics')
        for root, dirs, files in os.walk(graphics_path):
            for file in files:
                if file.endswith('.png'):
                    full_path = os.path.join(root, file)
                    relative_dir = full_path[full_path.rindex('graphics') + 8:].replace('\\', '/')
                    self.__cache[relative_dir] = pygame.image.load(full_path).convert_alpha()
        print(f'[{pygame.time.get_ticks()}] Sprites carregados')

    def get_sprite(self, file):
        file_dir = file.replace('\\', '/')
        return self.__cache[file_dir]
