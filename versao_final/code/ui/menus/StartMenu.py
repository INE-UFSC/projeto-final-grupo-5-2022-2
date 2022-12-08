from code.ui.components.Cursor import Cursor
from code.ui.components.Label import Label
from code.ui.menus.Menu import Menu


class StartMenu(Menu):
    def __init__(self):
        super().__init__()
        self.components = [Label({'center': (200, 200)}, 'START MENU', self.font),
                           Cursor()]
