import pygame
import os

from utils import load_sprite


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'tile'
        self.image = load_sprite(os.path.join('test', 'rock.png'))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -16)
        self.smaller_hitbox = self.rect.inflate(-16, -16)
