from abc import ABC, abstractmethod

import pygame

from code.Settings import *
from code.ui.UIComponent import UIComponent


class Button(UIComponent, pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, width, height, enabled=True, color=UI_BG_COLOR, hover_color=UI_HOVER_COLOR,
                 on_click_args=None, on_click=None):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.rect = pygame.Rect(x, y, width, height)
        self.__color = color
        self.__hover_color = hover_color
        self.__enabled = enabled

        self.__on_click_args = on_click_args
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
                    self.__on_click(self.__on_click_args)
                    self.__can_click = False

    @abstractmethod
    def draw(self):
        pass

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.__can_click and current_time - self.__click_time >= self.__click_cooldown:
            self.__can_click = True

    def button_update(self):
        self.cooldown()
        self.input()
        self.draw()

    @property
    def on_click_args(self):
        return self.__on_click_args

    @on_click_args.setter
    def on_click_args(self, index):
        self.__on_click_args = index

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

    @property
    def click_time(self):
        return self.__click_time

    @click_time.setter
    def click_time(self, click_time):
        self.__click_time = click_time

    @property
    def can_click(self):
        return self.__can_click

    @can_click.setter
    def can_click(self, can_click):
        self.__can_click = can_click