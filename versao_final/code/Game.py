import sys

import pygame

from code.library.Resources import Resources
from code.library.Settings import Settings
from code.scenes.DeathMenuScene import DeathMenuScene
from code.scenes.LevelScene import LevelScene
from code.scenes.StartMenuScene import StartMenuScene
from code.scenes.WinMenuScene import WinMenuScene


class Game:
    def __init__(self):
        pygame.init()
        self.__settings = Settings()
        self.screen = pygame.display.set_mode((self.__settings.WIDTH, self.__settings.HEIGHT))
        pygame.display.set_caption('Jornada à sala ALOCAR')
        self.clock = pygame.time.Clock()

        Resources()  # carregar os sprites

        self.__scenes = {'start': StartMenuScene(self.change_to_scene),
                         'level': LevelScene(self.change_to_scene),
                         'death': DeathMenuScene(self.change_to_scene),
                         'win': WinMenuScene(self.change_to_scene)}
        self.__current_scene_key = 'start'
        self._initialized = True

    def run(self):
        while True:
            current_scene = self.__scenes[self.__current_scene_key]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        if isinstance(current_scene,
                                      LevelScene):  # TODO: acho que dava só pra ter um método pra reagir a keys na cena
                            current_scene.toggle_menu()

            self.screen.fill(self.__settings.COLOR_BLACK)
            current_scene.run()
            pygame.display.update()
            self.clock.tick(self.__settings.FPS)

    def change_to_scene(self, scene):
        self.__current_scene_key = scene
        self.__scenes[self.__current_scene_key] = self.__scenes[self.__current_scene_key].__class__(
            self.change_to_scene)  # resetar as cenas ao trocar
