from code.scenes.Scene import Scene
from code.ui.menus.EndMenu import EndMenu


class DeathMenuScene(Scene):
    def __init__(self, change_to_scene):
        super().__init__(change_to_scene)
        self.__menu = EndMenu(self.change_to_scene, 'VOCÊ NÃO CHEGOU À SALA ALOCAR')

    def run(self):
        self.__menu.draw()
