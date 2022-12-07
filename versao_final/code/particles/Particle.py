from abc import abstractmethod, ABC

import pygame


class Particle(pygame.sprite.Sprite, ABC):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.inner_timer = 0  # um timer interno é mais suave que utilizar os ticks do pygame

    @abstractmethod
    def animate(self):
        pass

    def update(self):
        self.inner_timer += 1
        self.animate()
