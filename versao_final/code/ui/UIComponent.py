from abc import ABC, abstractmethod

import pygame.display


class UIComponent(ABC):
    def __init__(self):
        self.__display_surface = pygame.display.get_surface()

    @abstractmethod
    def draw(self):
        pass

    @property
    def display_surface(self):
        return self.__display_surface
