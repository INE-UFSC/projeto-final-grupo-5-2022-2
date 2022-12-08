from code.scenes.IScene import IScene
from code.ui.menus.StartMenu import StartMenu


class StartMenuScene(IScene):
    def __init__(self):
        self.__menu = StartMenu()

    def run(self):
        self.__menu.draw()
