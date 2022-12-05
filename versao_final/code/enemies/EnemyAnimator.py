import pygame
from code.Resources import Resources
from code.GroupManager import GroupManager


class EnemyAnimator:
    def __init__(self, name : str, animations : tuple) -> None:
        self.__animations = dict
        for animation in animations:
            self.__animations[animation] = Resources.get_animation(f'/enemies/{name}/{animation}')
        self.__group_manager = GroupManager()

    def tick(self, animation) -> bool:
        # returna True se está no último frame da animação
        player = self.__group_manager.player
        self.__frame_index += self.animation_speed
        if self.__frame_index >= len(self.animations[animation]):
            self.__frame_index = 0
        self.image = self.animations[animation][int(self.__frame_index)]
        if player.hitbox.x < self.__hitbox.x:
            # virar o inimigo em direção do player
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.hitbox.center)
        # animação de vulnerabilidade
        if not self.__vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    @property
    def animations(self) -> list:
        return self.__animations