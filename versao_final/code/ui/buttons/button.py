from abc import ABC, abstractmethod

import pygame

from code.settings import *


class Button(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, width, height, enabled=True, color=UI_BG_COLOR, hover_color=UI_HOVER_COLOR,
                 on_click_args=None, on_click=None):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.rect = pygame.Rect(x, y, width, height)
        self.__color = color
        self.__hover_color = hover_color
        self.__enabled = enabled

        self.__index = on_click_args
        self.__on_click = on_click
        self.__can_click = True
        self.__click_time = None
        self.__click_cooldown = 50  # para evitar que o usuário clique várias vezes sem querer

    def input(self):
        if self.__enabled:
            mouse_pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            if mouse[0] and self.rect.collidepoint(mouse_pos):
                self.__click_time = pygame.time.get_ticks()
                if self.__can_click:
                    self.__on_click(self.__index)
                    self.__can_click = False

    @abstractmethod
    def display(self):
        pass

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.__can_click and current_time - self.__click_time >= self.__click_cooldown:
            self.__can_click = True

    def button_update(self):
        self.cooldown()
        self.input()
        self.display()

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, index):
        self.__index = index

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, enabled):
        self.__enabled = enabled

    @property
    def color(self):
        return self.__color

    @property
    def hover_color(self):
        return self.__hover_color

    @property
    def display_surface(self):
        return self.__display_surface

    @property
    def font(self):
        return self.__font
