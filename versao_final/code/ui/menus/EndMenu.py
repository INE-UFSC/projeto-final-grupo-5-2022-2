from code.library.Settings import Settings
from code.ui.components.Cursor import Cursor
from code.ui.components.Image import Image
from code.ui.components.Label import Label
from code.ui.components.buttons.TextButton import TextButton
from code.ui.menus.Menu import Menu


class EndMenu(Menu):
    def __init__(self, change_to_scene, message):
        super().__init__()
        self.__settings = Settings()
        center_x = self.display_surface.get_width() // 2

        buttons = [TextButton(0, 416, 'Reiniciar', on_click=change_to_scene, on_click_args='new_level'),
                   TextButton(0, 512, 'Voltar ao Menu', on_click=change_to_scene, on_click_args='start')]

        for button in buttons:
            button.rect.centerx = center_x

        self.components = [Image({'centerx': center_x, 'top': self.__settings.MENU_LOGO_TOP}, '/logo.png'),
                           Label({'centerx': center_x, 'top': 320}, message, self.font, "#ff5f4f"), *buttons, Cursor()]
