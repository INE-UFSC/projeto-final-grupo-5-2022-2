import pygame

from code.utils import load_sprite


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.sprite_type = 'tile'
        self.image = load_sprite('/test/rock.png')
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -16)
        self.smaller_hitbox = self.rect.inflate(-16, -26)
        self.smaller_hitbox.y = self.rect.y
