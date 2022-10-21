import pygame

from settings import *


def load_sprite(file):
    return pygame.image.load(f'{GRAPHICS_PATH}{file}').convert_alpha()
