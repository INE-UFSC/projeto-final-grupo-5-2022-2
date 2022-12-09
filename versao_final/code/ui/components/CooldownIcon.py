import pygame

from code.library.Settings import Settings
from code.ui.components.UIComponent import UIComponent


class CooldownIcon(UIComponent):
    def __init__(self, pos, icon, current_cooldown, maximum_cooldown, background_color, cooldown_alpha=128,
                 outline_width=3):
        super().__init__()
        self.__settings = Settings()
        self.__icon = icon
        self.__current_cooldown = current_cooldown
        self.__maximum_cooldown = maximum_cooldown
        self.__background_color = background_color
        self.__cooldown_alpha = cooldown_alpha
        self.__outline_width = outline_width
        self.__rect = pygame.Rect(pos[0], pos[1], self.__settings.ITEM_BOX_SIZE, self.__settings.ITEM_BOX_SIZE)

    def draw(self):
        pygame.draw.rect(self.display_surface, self.__background_color, self.__rect)
        self.display_surface.blit(self.__icon, self.__rect)

        # cooldown
        if self.__current_cooldown > 0:
            cooldown_rect_height = self.__settings.ITEM_BOX_SIZE - self.__settings.ITEM_BOX_SIZE * (
                    self.__maximum_cooldown - self.__current_cooldown) / self.__maximum_cooldown
            rect_height = max(1, cooldown_rect_height)  # aqui tem que usar o max() para não resultar em altura 0
            cooldown_surf = pygame.Surface((self.__settings.ITEM_BOX_SIZE, rect_height))
            cooldown_surf.set_alpha(self.__cooldown_alpha)
            cooldown_surf.fill(self.__settings.COLOR_BLACK)
            self.display_surface.blit(cooldown_surf, self.__rect)

        pygame.draw.rect(self.display_surface, self.__settings.UI_BORDER_COLOR, self.__rect, self.__outline_width)

    @property
    def icon(self):
        return self.__icon

    @icon.setter
    def icon(self, icon):
        self.__icon = icon

    @property
    def current_cooldown(self):
        return self.__current_cooldown

    @current_cooldown.setter
    def current_cooldown(self, current_cooldown):
        self.__current_cooldown = current_cooldown

    @property
    def maximum_cooldown(self):
        return self.__maximum_cooldown

    @maximum_cooldown.setter
    def maximum_cooldown(self, maximum_cooldown):
        self.__maximum_cooldown = maximum_cooldown
