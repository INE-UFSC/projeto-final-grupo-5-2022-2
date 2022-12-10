import pygame

from code.library.Resources import Resources
from code.library.Settings import Settings
from code.ui.components.CooldownIcon import CooldownIcon
from code.ui.components.Cursor import Cursor
from code.ui.components.Label import Label
from code.ui.components.ProgressBar import ProgressBar
from code.ui.menus.LevelMenu import LevelMenu


class LevelUI:
    def __init__(self):
        self.__settings = Settings()
        self.__display_surface = pygame.display.get_surface()
        self.__font = pygame.font.Font(self.__settings.UI_FONT, self.__settings.UI_FONT_SIZE)

        self.__health_sprite = Resources().get_sprite('/icons/heart.png')

        self.__exp_bar = ProgressBar((0, 0), 0, 0, self.__settings.EXP_BAR_WIDTH, self.__settings.BAR_HEIGHT,
                                     self.__settings.UI_BG_COLOR, self.__settings.EXP_BAR_COLOR, 3)
        self.__exp_bar.rect.topright = (self.__display_surface.get_size()[0] - 20, 10)
        exp_label_x = self.__display_surface.get_size()[0] - 30
        exp_label_y = self.__settings.BAR_HEIGHT + 17
        exp_label_pos = {'topright': (exp_label_x, exp_label_y)}
        self.__exp_label = Label(exp_label_pos, '', self.__font, self.__settings.TEXT_COLOR)

        up_x = self.__display_surface.get_size()[0] - 20
        up_y = self.__display_surface.get_size()[1] - 20
        upgrade_points_pos = {'bottomright': (up_x, up_y)}
        self.__upgrade_points_label = Label(upgrade_points_pos, '', self.__font, self.__settings.TEXT_COLOR)

        tl_x = self.__display_surface.get_width() // 2
        tl_y = 20
        timer_label_pos = {'centerx': tl_x, 'top': tl_y}
        self.__timer_label = Label(timer_label_pos, '', self.__font, self.__settings.TEXT_COLOR)

        self.__cooldown_icons = []  # a lista de ícones é gerada no show_cooldowns()

        self.__level_menu = LevelMenu()

        self.__cursor = Cursor()

    def show_health(self, health):
        for i in range(health):
            x = 10 + i * (self.__settings.ITEM_BOX_SIZE + self.__settings.UI_COMPONENT_MARGIN)
            y = 10
            self.__display_surface.blit(self.__health_sprite,
                                        self.__health_sprite.get_rect(topleft=(x, y)))

    def show_exp(self, exp, level_up_exp, current_level):
        # barra
        self.__exp_bar.current_progress = exp
        self.__exp_bar.maximum_progress = level_up_exp
        self.__exp_bar.draw()
        # nível atual
        self.__exp_label.text = f'LV: {current_level}'
        self.__exp_label.draw()

    def show_cooldowns(self, attacks):
        if len(self.__cooldown_icons) != len(attacks):
            self.__cooldown_icons = []
            for i, attack in enumerate(attacks):
                x = self.__settings.UI_COMPONENT_MARGIN + i * (
                            self.__settings.ITEM_BOX_SIZE + self.__settings.UI_COMPONENT_MARGIN)
                y = self.__settings.HEIGHT - self.__settings.UI_COMPONENT_MARGIN - self.__settings.ITEM_BOX_SIZE
                self.__cooldown_icons.append(CooldownIcon((x, y), attack.icon, attack.attack_time, attack.cooldown,
                                                          self.__settings.UI_BG_COLOR))

        for i, cooldown_icon in enumerate(self.__cooldown_icons):
            cooldown_icon.current_cooldown = attacks[i].attack_time
            cooldown_icon.maximum_cooldown = attacks[i].cooldown
            cooldown_icon.draw()

    def show_upgrade_points(self, upgrade_points):
        self.__upgrade_points_label.text = str(upgrade_points)
        self.__upgrade_points_label.draw()

    def toggle_menu(self):
        self.__level_menu.toggle()

    def show_cursor(self):
        self.__cursor.draw()

    def show_timer(self, time):
        if time == self.__settings.WAVE_TIME:
            # não mostrar o timer caso a wave tenha acabado
            return

        remaining_time = self.__settings.WAVE_TIME - time
        total_seconds = remaining_time // 60
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        self.__timer_label.text = f'{minutes}:{seconds:02d}'
        self.__timer_label.draw()

    @property
    def is_menu_open(self):
        return self.__level_menu.is_open

    @property
    def exit_clicked(self):
        return self.__level_menu.exit_clicked

    def display(self, player, time):
        self.show_timer(time)
        self.show_health(player.health)
        self.show_exp(player.exp, player.level_up_exp, player.current_level)
        self.show_cooldowns(player.attacks)
        self.show_upgrade_points(player.upgrade_points)

        if self.is_menu_open:
            self.__level_menu.draw()

        self.show_cursor()
