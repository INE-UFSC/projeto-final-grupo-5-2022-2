import pygame
import os

from settings import *

def load_sprite(file_path):
    path = os.path.join(GAME_PATH, 'graphics', file_path)
    return pygame.image.load(path).convert_alpha()


def load_sound(file_name):
    return pygame.mixer.Sound(os.path.join(GAME_PATH, 'audio', file_name))
