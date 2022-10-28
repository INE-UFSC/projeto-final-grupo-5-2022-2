import pygame

from settings import *
from utils import load_sprite


class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.health_sprite = load_sprite('/test/heart.png')

    def show_health(self, health):
        for i in range(health):
            self.display_surface.blit(self.health_sprite,
                                      self.health_sprite.get_rect(topleft=(10 + i * (ITEM_BOX_SIZE + 10), 10)))

    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def show_attacks(self, selected_attack, attacks):
        current_time = pygame.time.get_ticks()

        for i, attack in enumerate(attacks):
            bg_rect = pygame.Rect(10 + i * (ITEM_BOX_SIZE + 10), HEIGHT - 10 - ITEM_BOX_SIZE, ITEM_BOX_SIZE,
                                  ITEM_BOX_SIZE)
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

            # ícone
            attack_surf = attack.icon
            attack_rect = attack_surf.get_rect(center=bg_rect.center)
            self.display_surface.blit(attack_surf, attack_rect)

            # cooldown
            if not attack.can_attack:
                # aqui tem que usar o max() para não resultar em altura 0
                rect_height = max(1,
                                  ITEM_BOX_SIZE - ITEM_BOX_SIZE * (current_time - attack.attack_time) / attack.cooldown)
                cooldown_surf = pygame.Surface((ITEM_BOX_SIZE, rect_height))
                cooldown_surf.set_alpha(128)
                cooldown_surf.fill(COLOR_BLACK)
                self.display_surface.blit(cooldown_surf, bg_rect)

            # seleção
            if i == selected_attack - 1:
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, bg_rect, 3)
            else:
                pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def display(self, player):
        self.show_health(player.health)
        self.show_exp(player.exp)
        self.show_attacks(player.selected_attack, player.attacks)
