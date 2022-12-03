import pygame

from code.Settings import *
from code.ui.UIComponent import UIComponent


class Label(UIComponent):
    def __init__(self, pos_kwargs, text, font, text_color=TEXT_COLOR):
        super().__init__()
        self.__pos_kwargs = pos_kwargs
        self.__text = text
        self.__font = font
        self.__text_color = text_color

    def draw(self):
        text_surf = self.__font.render(self.__text, False, self.__text_color)
        text_rect = text_surf.get_rect(**self.__pos_kwargs)

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, text):
        self.__text = text
