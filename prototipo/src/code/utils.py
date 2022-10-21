from importlib.resources import path
import os
from settings import *
import pygame


def load_sprite(file):
    return pygame.image.load(f'{GRAPHICS_PATH}{file}').convert_alpha()
