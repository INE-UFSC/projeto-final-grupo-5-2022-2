import pygame

from settings import *


def load_sprite(file):
    return pygame.image.load(f'{GAME_PATH}/graphics/{file}').convert_alpha()


def load_sound(file):
    return pygame.mixer.Sound(f'{GAME_PATH}/audio/{file}')
