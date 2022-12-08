from abc import ABC

import pygame

from code.Settings import UI_FONT, UI_FONT_SIZE
from code.ui.components.buttons.Button import Button


class Menu(ABC):
    def __init__(self):
        self.__font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.__components = None

    def draw(self):
        for component in self.__components:
            if isinstance(component, Button):
                component.button_update()
            else:
                component.draw()

    @property
    def font(self):
        return self.__font

    @property
    def components(self):
        return self.__components

    @components.setter
    def components(self, components):
        self.__components = components
