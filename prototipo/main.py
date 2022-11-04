import sys

import pygame

from code.level import Level as Level
from code.settings import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Jornada à sala ALOCAR')
        self.clock = pygame.time.Clock()
        # level
        self.level = Level()
        self.run()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.level.toggle_menu()

            self.screen.fill(COLOR_BLACK)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
