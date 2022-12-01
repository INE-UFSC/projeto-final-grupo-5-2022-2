import pygame

from code.resources import Resources


class Cursor:
    def __init__(self, image_path):
        self.__display_surface = pygame.display.get_surface()
        self.__cursor = Resources().get_sprite(image_path)
        pygame.mouse.set_visible(False)

    def draw(self):
        x, y = pygame.mouse.get_pos()
        x -= self.__cursor.get_width() // 2
        y -= self.__cursor.get_height() // 2
        self.__display_surface.blit(self.__cursor, (x, y))
