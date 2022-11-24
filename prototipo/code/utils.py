from csv import reader
from os import walk

import pygame

from code.settings import *
from code.sprite_manager import SpriteManager


def load_sound(file):
    return pygame.mixer.Sound(f'{GAME_PATH}/audio/{file}')


def load_objects(room_name):
    tiles = list()
    with open(f'{GAME_PATH}/rooms/{room_name}/objects.csv') as tiles_csv:
        layout = reader(tiles_csv, delimiter=',')
        for row in layout:
            tiles.append(row)
    return tiles


def get_animation(folder_name):
    surface_list = []
    for _, __, img_files in walk(f'{GAME_PATH}/graphics/{folder_name}'):
        for image in img_files:
            image_surf = SpriteManager().get_sprite(f'{folder_name}/{image}')
            surface_list.append(image_surf)
    return surface_list
