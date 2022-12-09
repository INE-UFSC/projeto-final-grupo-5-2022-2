import random

import pygame

from code.level.GroupManager import GroupManager
from code.level.upgrades import FireRateUpgrade
from code.level.upgrades import HealthUpgrade, DamageUpgrade, SpeedUpgrade
from code.library.Settings import Settings
from code.ui.components.UIComponent import UIComponent
from code.ui.components.buttons.TextButton import TextButton
from code.ui.components.buttons.UpgradeButton import UpgradeButton


class UpgradeMenu(UIComponent):
    def __init__(self):
        super().__init__()
        self.__settings = Settings()
        self.__font = pygame.font.Font(self.__settings.UI_FONT, self.__settings.UI_FONT_SIZE)
        self.__is_open = False
        self.__available_upgrades = {'health': HealthUpgrade.HealthUpgrade(), 'damage': DamageUpgrade.DamageUpgrade(),
                                     'firerate': FireRateUpgrade.FireRateUpgrade(),
                                     'speed': SpeedUpgrade.SpeedUpgrade()}
        self.__upgrade_buttons = []
        self.reroll_upgrades()

        self.__exit_button = TextButton(self.__settings.UI_COMPONENT_MARGIN,
                                        self.__settings.HEIGHT - self.__settings.UI_COMPONENT_MARGIN - self.__settings.TEXT_BUTTON_HEIGHT,
                                        'SAIR PARA A TELA INICIAL',
                                        on_click=self.exit,
                                        on_click_args=None,
                                        width=self.__settings.EXIT_BUTTON_WIDTH)
        self.__exit_clicked = False

    def exit(self):
        self.__exit_clicked = True

    @property
    def exit_clicked(self):
        return self.__exit_clicked

    def toggle(self):
        self.__is_open = not self.__is_open

    @property
    def is_open(self):
        return self.__is_open

    def reroll_upgrades(self):
        self.__upgrade_buttons = list()
        remaining_upgrades = list(self.__available_upgrades.values())
        for i in range(0, 3):
            x = self.display_surface.get_size()[0] - self.__settings.UPGRADE_BUTTON_RIGHT_MARGIN
            y = self.__settings.UPGRADE_BUTTON_TOP + self.__settings.UPGRADE_BUTTON_SPACING * i
            upgrade = random.choice(remaining_upgrades)
            button = UpgradeButton(x, y, on_click_args=upgrade, on_click=self.buy_upgrade)
            self.__upgrade_buttons.append(button)
            remaining_upgrades.remove(upgrade)
            if len(remaining_upgrades) == 0:
                break

    def buy_upgrade(self, upgrade):
        GroupManager().player.give_upgrade(upgrade)
        self.reroll_upgrades()

    def draw(self):
        player = GroupManager().player
        # fundo
        shadow = pygame.Surface(self.display_surface.get_size())
        shadow.set_alpha(150)
        shadow.fill(self.__settings.COLOR_BLACK)
        self.display_surface.blit(shadow, (0, 0))

        # seção de stats
        stats = {'HP': f'{player.health}/{player.max_health}',
                 'DAMAGE': f'+{int((player.attacks[0].damage - player.attacks[0].base_damage) / player.attacks[0].base_damage * 100)}%',
                 'FIRERATE': f'+{int((player.attacks[0].base_cooldown - player.attacks[0].cooldown) / player.attacks[0].base_cooldown * 100)}%',
                 'SPEED': f'+{int((player.move_speed - player.base_speed) / player.base_speed * 100)}%'}

        for i, key in enumerate(stats):
            x = self.__settings.STAT_LEFT_MARGIN
            y = self.__settings.STAT_TOP_MARGIN + self.__settings.STAT_SPACING * i

            stat_name_surf = self.__font.render(f'{key}', False, self.__settings.TEXT_COLOR)
            stat_name_rect = stat_name_surf.get_rect(topleft=(x, y))
            stat_surf = self.__font.render(f'{stats[key]}', False, self.__settings.TEXT_COLOR)
            stat_rect = stat_surf.get_rect(topright=(x + self.__settings.STAT_BAR_WIDTH, y))
            self.display_surface.blit(stat_name_surf, stat_name_rect)
            self.display_surface.blit(stat_surf, stat_rect)
            separator = pygame.Rect(stat_name_rect.left, stat_name_rect.bottom + 5,
                                    self.__settings.STAT_BAR_WIDTH, 4)
            pygame.draw.rect(self.display_surface, self.__settings.UI_BORDER_COLOR_ACTIVE, separator)

        # seção de upgrades
        for button in self.__upgrade_buttons:
            button.enabled = player.upgrade_points > 0
            button.button_update()

        upgrade_title_surf = self.__font.render('UPGRADES DISPONÍVEIS', False, self.__settings.TEXT_COLOR)
        ut_x = self.display_surface.get_size()[0] - self.__settings.UPGRADE_BUTTON_RIGHT_MARGIN
        ut_y = self.__settings.UPGRADE_TITLE_TOP
        upgrade_title_rect = upgrade_title_surf.get_rect(
            topleft=(ut_x, ut_y))
        self.display_surface.blit(upgrade_title_surf, upgrade_title_rect)

        # botão de sair para o menu
        self.__exit_button.button_update()
