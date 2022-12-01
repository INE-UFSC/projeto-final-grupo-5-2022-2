import pygame

from code.settings import *


class ProgressBar:
    def __init__(self, pos, current_progress, maximum_progress, width=EXP_BAR_WIDTH, height=BAR_HEIGHT,
                 background_color=UI_BG_COLOR, progress_color=EXP_BAR_COLOR, outline_width=3):
        self.__display_surface = pygame.display.get_surface()
        self.__pos = pos
        self.__current_progress = current_progress
        self.__maximum_progress = maximum_progress
        self.__background_color = background_color
        self.__progress_color = progress_color
        self.__outline_width = outline_width
        self.__rect = pygame.Rect(0, 0, width, height)

    def draw(self):
        pygame.draw.rect(self.__display_surface, self.__background_color, self.__rect)
        ratio = self.__current_progress / self.__maximum_progress
        current_width = self.__rect.width * ratio
        current_rect = self.__rect.copy()
        current_rect.width = current_width
        pygame.draw.rect(self.__display_surface, self.__progress_color, current_rect)
        pygame.draw.rect(self.__display_surface, UI_BORDER_COLOR, self.__rect, self.__outline_width)

    @property
    def current_progress(self):
        return self.__current_progress

    @current_progress.setter
    def current_progress(self, current_progress):
        self.__current_progress = current_progress

    @property
    def maximum_progress(self):
        return self.__maximum_progress

    @maximum_progress.setter
    def maximum_progress(self, maximum_progress):
        self.__maximum_progress = maximum_progress

    @property
    def rect(self):
        return self.__rect
