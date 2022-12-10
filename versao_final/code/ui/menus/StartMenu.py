import sys

import pygame

from code.library.Settings import Settings
from code.ui.components.Cursor import Cursor
from code.ui.components.Image import Image
from code.ui.components.buttons.TextButton import TextButton
from code.ui.menus.Menu import Menu
from code.library.Resources import Resources


class StartMenu(Menu):
    def __init__(self, change_to_scene):
        super().__init__()
        self.__settings = Settings()
        self.__resources = Resources()
        center_x = self.display_surface.get_width() // 2
        self.__change_to_scene = change_to_scene

        buttons = [TextButton(0, 320, 'NOVO JOGO', on_click=self.new_level, on_click_args=None),
                   TextButton(0, 416, 'CONTINUAR', on_click=self.to_level, on_click_args='level'),
                   TextButton(0, 512, 'SAIR', on_click=self.quit_game, on_click_args=None)]
        for button in buttons:
            button.rect.centerx = center_x

        buttons[1].enabled = self.__resources.has_save()

        self.components = [Image({'centerx': center_x, 'top': self.__settings.MENU_LOGO_TOP}, '/logo.png'), *buttons, Cursor()]

    def to_level(self, key):
        self.__change_to_scene(key)

    def new_level(self):
        self.__settings.new_game = True
        self.__change_to_scene('level')

    def quit_game(self):
        pygame.quit()
        sys.exit()