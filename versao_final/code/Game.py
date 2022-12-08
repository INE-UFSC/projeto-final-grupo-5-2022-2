import sys

import pygame

from code.Resources import Resources
from code.Settings import *
from code.Singleton import Singleton
from code.scenes.LevelScene import LevelScene
from code.scenes.StartMenuScene import StartMenuScene


class Game(Singleton):
    def __init__(self):
        if not self._initialized:
            pygame.init()
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Jornada à sala ALOCAR')
            self.clock = pygame.time.Clock()
            Resources()  # carregar os sprites
            self.__scenes = (StartMenuScene(), LevelScene())
            self.__scenes = {'start': StartMenuScene(),
                             'level': LevelScene()}
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
                        if isinstance(current_scene, LevelScene):  # TODO: acho que dava só pra ter um método pra reagir a keys na cena
                            current_scene.toggle_menu()

            self.screen.fill(COLOR_BLACK)
            current_scene.run()
            pygame.display.update()
            self.clock.tick(FPS)
