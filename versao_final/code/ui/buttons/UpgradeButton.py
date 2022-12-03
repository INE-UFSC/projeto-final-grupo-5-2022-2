import pygame

from code.Settings import *
from code.ui.buttons.Button import Button


class UpgradeButton(Button):
    def __init__(self, x, y, on_click_args, on_click):
        super().__init__(x, y, UPGRADE_BUTTON_WIDTH, UPGRADE_BUTTON_HEIGHT, on_click_args=on_click_args, on_click=on_click)

    def draw(self):
        if self.enabled:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                # hover
                pygame.draw.rect(self.display_surface, self.hover_color, self.rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, self.rect, 4)
            else:
                # normal
                pygame.draw.rect(self.display_surface, self.color, self.rect)
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.rect, 4)

            # conteúdo
            # nome
            name_surf = self.font.render(self.on_click_args.name, False, TEXT_COLOR)
            name_rect = name_surf.get_rect(topleft=(self.rect.left + 10, self.rect.top + 10))
            self.display_surface.blit(name_surf, name_rect)
            # linha pra separar
            separator = pygame.Rect(name_rect.left, name_rect.bottom + 5, self.rect.width - 20, 4)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, separator)
            # ícone
            icon = self.on_click_args.icon
            icon_rect = icon.get_rect(topleft=(name_rect.left, separator.bottom + 10))
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, icon_rect, 4)
            self.display_surface.blit(icon, icon_rect)
            # descrição
            description_surf = pygame.Surface((482, 64)).convert_alpha()
            description_surf.fill([0, 0, 0, 0])
            description_rect = name_surf.get_rect(topleft=(icon_rect.right + 10, icon_rect.top))
            # separar as linhas da descrição
            words = self.on_click_args.description.split(' ')
            current_line = 0
            while len(words) > 0:
                current_word_index = len(words)
                # escrever removendo a cada iteração a última palavra
                # até que caiba dentro do retângulo da descrição
                while True:
                    line_text = ' '.join(words[0:current_word_index])
                    line_surf = self.font.render(line_text, False, TEXT_COLOR)
                    if line_surf.get_size()[0] <= description_surf.get_size()[0]:
                        break
                    else:
                        current_word_index -= 1
                # desenhar a linha atual
                description_surf.blit(line_surf, (0, current_line * 22))
                # remover as palavras utilizadas na última linha
                words = words[current_word_index:len(words)]
                current_line += 1
            # desenhar descrição
            self.display_surface.blit(description_surf, description_rect)
        else:
            disabled_background = pygame.Surface(self.rect.size)
            disabled_background.fill(UI_BORDER_COLOR)
            self.display_surface.blit(disabled_background, self.rect.topleft)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.rect, 4)

            # texto de indisponível
            msg_surf = self.font.render('VOCÊ NÃO POSSUI PONTOS DE UPGRADE!', False, TEXT_COLOR)
            msg_rect = msg_surf.get_rect(center=self.rect.center)
            self.display_surface.blit(msg_surf, msg_rect)
