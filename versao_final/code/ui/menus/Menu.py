from abc import ABC

import pygame

from code.library.Settings import Settings
from code.ui.components.buttons.Button import Button


class Menu(ABC):
    def __init__(self):
        self.__settings = Settings()
        self.__display_surface = pygame.display.get_surface()
        self.__font = pygame.font.Font(self.__settings.UI_FONT, self.__settings.UI_FONT_SIZE)
        self.__components = None

    def draw(self):
        for component in self.__components:
            if isinstance(component, Button):
                component.button_update()
            else:
                component.draw()

    @property
    def display_surface(self):
        return self.__display_surface

    @property
    def font(self):
        return self.__font

    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, components):
        self.__components = components
