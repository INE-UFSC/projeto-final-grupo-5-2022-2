from code.scenes.IScene import IScene
from code.ui.menus.StartMenu import StartMenu


class StartMenuScene(IScene):
    def __init__(self, change_to_scene):
        self.__menu = StartMenu(change_to_scene)

    def run(self):
        self.__menu.draw()
