from code.scenes.Scene import Scene
from code.ui.menus.StartMenu import StartMenu


class StartMenuScene(Scene):
    def __init__(self, change_to_scene):
        super().__init__(change_to_scene)
        self.__menu = StartMenu(self.change_to_scene)

    def run(self):
        self.__menu.draw()
