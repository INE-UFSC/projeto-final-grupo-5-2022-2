import pygame

from code.resources import Resources
from code.ui.ui_component import UIComponent


class Cursor(UIComponent):
    def __init__(self, image_path):
        super().__init__()
        self.__cursor = Resources().get_sprite(image_path)
        pygame.mouse.set_visible(False)

    def draw(self):
        x, y = pygame.mouse.get_pos()
        x -= self.__cursor.get_width() // 2
        y -= self.__cursor.get_height() // 2
        self.display_surface.blit(self.__cursor, (x, y))
