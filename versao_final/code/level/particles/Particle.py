from abc import abstractmethod, ABC

import pygame


class Particle(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__inner_timer = 0  # um timer interno é mais suave que utilizar os ticks do pygame

    @abstractmethod
    def animate(self):
        pass

    def update(self):
        self.__inner_timer += 1
        self.animate()

    @property
    def inner_timer(self):
        return self.__inner_timer

    @property
    def display_surface(self):
        return self.__display_surface
