import sys

import pygame

from code.library.Settings import Settings
from code.ui.components.Cursor import Cursor
from code.ui.components.Image import Image
from code.ui.components.buttons.TextButton import TextButton
from code.ui.menus.Menu import Menu


class StartMenu(Menu):
    def __init__(self, change_to_scene):
        super().__init__()
        self.__settings = Settings()
        center_x = self.display_surface.get_width() // 2

        buttons = [TextButton(0, 320, 'NOVO JOGO', on_click=change_to_scene, on_click_args='level'),
                   TextButton(0, 416, 'CONTINUAR', None, None),
                   TextButton(0, 512, 'SAIR', on_click=self.quit_game, on_click_args=None)]
        for button in buttons:
            button.rect.centerx = center_x

        buttons[1].enabled = False

        self.components = [Image({'centerx': center_x, 'top': self.__settings.MENU_LOGO_TOP}, '/logo.png'), *buttons, Cursor()]

    def quit_game(self):
        pygame.quit()
        sys.exit()