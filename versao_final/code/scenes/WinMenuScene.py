from code.scenes.Scene import Scene
from code.ui.menus.EndMenu import EndMenu


class WinMenuScene(Scene):
    def __init__(self, change_to_scene):
        super().__init__(change_to_scene)
        message = 'PARABÉNS! VOCÊ COMPLETOU O JOGO'
        self.__menu = EndMenu(self.change_to_scene, message)

    def run(self):
        self.__menu.draw()
