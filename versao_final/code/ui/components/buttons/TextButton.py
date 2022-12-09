import pygame

from code.library.Settings import Settings
from code.ui.components.buttons.Button import Button


class TextButton(Button):
    def __init__(self, x, y, text, on_click_args, on_click, width=None):
        self.__settings = Settings()
        button_width = self.__settings.TEXT_BUTTON_WIDTH if width is None else width
        super().__init__(x, y, button_width, self.__settings.TEXT_BUTTON_HEIGHT,
                         self.__settings.UI_BG_COLOR, self.__settings.UI_HOVER_COLOR, 
                         on_click_args=on_click_args, on_click=on_click)
        self.__text = text

    def draw(self):
        text_surf = self.font.render(self.__text, False, self.__settings.TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)

        if self.enabled:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                # hover
                pygame.draw.rect(self.display_surface, self.hover_color, self.rect)
                pygame.draw.rect(self.display_surface, self.__settings.UI_BORDER_COLOR_ACTIVE, self.rect, 4)
            else:
                # normal
                pygame.draw.rect(self.display_surface, self.color, self.rect)
                pygame.draw.rect(self.display_surface, self.__settings.UI_BORDER_COLOR, self.rect, 4)
        else:
            pygame.draw.rect(self.display_surface, self.__settings.UI_BORDER_COLOR, self.rect)
            pygame.draw.rect(self.display_surface, self.__settings.UI_BORDER_COLOR, self.rect, 4)
            text_surf.set_alpha(150)

        self.display_surface.blit(text_surf, text_rect)
