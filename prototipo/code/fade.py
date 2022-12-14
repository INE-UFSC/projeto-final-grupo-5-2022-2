import pygame

from code.settings import *

class Fade(pygame.sprite.Sprite):
    def __init__(self, *groups, fade_step = 5, fade_in=True):
        super().__init__(groups)
        self.__sprite_type = 'fade'
        
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.fill(COLOR_BLACK)
        self.rect = self.image.get_rect()

        if fade_in:
            self.__fade_step = -abs(fade_step)
            self.image.set_alpha(255 + self.__fade_step)
        else:
            self.__fade_step = abs(fade_step)
            self.image.set_alpha(0 + self.__fade_step)
    
    @property
    def sprite_type(self):
        return self.__sprite_type

    def step(self) -> bool:
        print(self.image.get_alpha())
        # retorna True se o fade acabou
        if self.image.get_alpha() == 0 or self.image.get_alpha() == 255:
            return True
        else:
            self.image.set_alpha(self.image.get_alpha() + self.__fade_step)
            return False