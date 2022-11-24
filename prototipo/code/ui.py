import random

import pygame

from code.settings import *
from code.upgrade import *


class UI:
    def __init__(self):
        self.__display_surface = pygame.display.get_surface()
        self.__font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.__timer_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE + 6)

        self.__health_sprite = SpriteManager().get_sprite('/test/heart.png')
        self.__exp_bar_rect = pygame.Rect(0, 0, EXP_BAR_WIDTH, BAR_HEIGHT)
        self.__exp_bar_rect.topright = (self.display_surface.get_size()[0] - 20, 10)

        self.__is_menu_open = False
        self.__upgrade_button_list = []
        self.__available_upgrades = {'health': HealthUpgrade(), 'damage': DamageUpgrade(),
                                     'firerate': FireRateUpgrade(), 'speed': SpeedUpgrade()}

        pygame.mouse.set_visible(False)
        self.__cursor = SpriteManager().get_sprite('/cursor.png')

    @property
    def display_surface(self):
        return self.__display_surface

    @property
    def font(self):
        return self.__font

    @property
    def timer_font(self):
        return self.__timer_font

    @property
    def health_sprite(self):
        return self.__health_sprite

    @property
    def exp_bar_react(self):
        return self.__exp_bar_rect

    @property
    def is_menu_open(self):
        return self.__is_menu_open

    @property
    def upgrade_botton_list(self):
        return self.__upgrade_button_list

    @property
    def avalaible_upgrade(self):
        return self.__available_upgrades

    def show_health(self, health):
        for i in range(health):
            self.display_surface.blit(self.health_sprite,
                                      self.health_sprite.get_rect(topleft=(10 + i * (ITEM_BOX_SIZE + 10), 10)))

    def show_exp(self, exp, level_up_exp, current_level):
        # barra
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.__exp_bar_rect)

        ratio = exp / level_up_exp
        current_width = self.__exp_bar_rect.width * ratio
        current_rect = self.__exp_bar_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, EXP_BAR_COLOR, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, self.__exp_bar_rect, 3)

        # nível atual
        text_surf = self.font.render(str(f'LV: {current_level}'), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 30
        y = 10 + BAR_HEIGHT + 7
        text_rect = text_surf.get_rect(topright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def show_attacks(self, attacks):
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
                                  ITEM_BOX_SIZE - ITEM_BOX_SIZE * (
                                          attack.cooldown - attack.attack_time) / attack.cooldown)
                cooldown_surf = pygame.Surface((ITEM_BOX_SIZE, rect_height))
                cooldown_surf.set_alpha(128)
                cooldown_surf.fill(COLOR_BLACK)
                self.display_surface.blit(cooldown_surf, bg_rect)

            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_upgrade_points(self, upgrade_points):
        text_surf = self.font.render(str(int(upgrade_points)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def toggle_menu(self):
        self.__is_menu_open = not self.__is_menu_open

    def show_menu(self, player):
        # fundo
        shadow = pygame.Surface(self.display_surface.get_size())
        shadow.set_alpha(150)
        shadow.fill(COLOR_BLACK)
        self.display_surface.blit(shadow, (0, 0))

        # seção de stats
        stats = {'HP': f'{player.health}/{player.max_health}',
                 'DAMAGE': f'+{int((player.attacks[0].damage - player.attacks[0].base_damage) / player.attacks[0].base_damage * 100)}%',
                 'FIRERATE': f'+{int((player.attacks[0].base_cooldown - player.attacks[0].cooldown) / player.attacks[0].base_cooldown * 100)}%',
                 'SPEED': f'+{int((player.move_speed - player.base_speed) / player.base_speed * 100)}%'}

        for i, key in enumerate(stats):
            x, y = 128, 256 + 64 * i
            stat_name_surf = self.font.render(f'{key}', False, TEXT_COLOR)
            stat_name_rect = stat_name_surf.get_rect(topleft=(x, y))
            stat_surf = self.font.render(f'{stats[key]}', False, TEXT_COLOR)
            stat_rect = stat_surf.get_rect(topright=(x + STAT_BAR_WIDTH, y))
            self.display_surface.blit(stat_name_surf, stat_name_rect)
            self.display_surface.blit(stat_surf, stat_rect)
            separator = pygame.Rect(stat_name_rect.left, stat_name_rect.bottom + 5, STAT_BAR_WIDTH, 4)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, separator)

        # seção de upgrades
        for button in self.__upgrade_button_list:
            button.enabled = player.upgrade_points > 0
            button.button_update()

        upgrade_title_surf = self.font.render('UPGRADES DISPONÍVEIS', False, TEXT_COLOR)
        upgrade_title_rect = upgrade_title_surf.get_rect(topleft=(self.display_surface.get_size()[0] - 704, 64))
        self.display_surface.blit(upgrade_title_surf, upgrade_title_rect)

    def reroll_upgrades(self):
        remaining_upgrades = list(self.__available_upgrades.values())
        for i in range(0, 3):
            upgrade = random.choice(remaining_upgrades)
            self.__upgrade_button_list[i].index[1] = upgrade
            remaining_upgrades.remove(upgrade)
            if len(remaining_upgrades) == 0:
                break

    def buy_upgrade(self, args):
        # essa função vai receber como args o give_upgrade() do player e o upgrade
        args[0](args[1])
        self.reroll_upgrades()

    def show_cursor(self):
        x, y = pygame.mouse.get_pos()
        x -= self.__cursor.get_width() // 2
        y -= self.__cursor.get_height() // 2
        self.display_surface.blit(self.__cursor, (x, y))

    def show_timer(self, time):
        if time == WAVE_TIME:
            # não mostrar o timer caso a wave tenha acabado
            return

        remaining_time = WAVE_TIME - time
        total_seconds = remaining_time // 60
        minutes = total_seconds // 60
        seconds = total_seconds % 60

        time_surf = self.font.render(f'{minutes}:{seconds:02d}', False, TEXT_COLOR)
        time_rect = time_surf.get_rect(topleft=(self.display_surface.get_width() // 2 - time_surf.get_width() // 2, 20))
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, time_rect.inflate(20, 20))
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, time_rect.inflate(20, 20), 3)
        self.display_surface.blit(time_surf, time_rect)

    def display(self, player, time):
        if len(self.__upgrade_button_list) == 0:
            # iniciar os botões de upgrade
            for i in range(0, 3):
                x = self.display_surface.get_size()[0] - 704
                y = 128 + 192 * i
                button = UpgradeButton(x, y, [player.give_upgrade, self.__available_upgrades['health']],
                                       on_click=self.buy_upgrade)
                self.__upgrade_button_list.append(button)
            self.reroll_upgrades()

        self.show_timer(time)
        self.show_health(player.health)
        self.show_exp(player.exp, player.level_up_exp, player.current_level)
        self.show_attacks(player.attacks)
        self.show_upgrade_points(player.upgrade_points)

        if self.__is_menu_open:
            self.show_menu(player)

        self.show_cursor()

    @property
    def is_menu_open(self):
        return self.__is_menu_open


class Button(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, width, height, index, enabled=True, color=UI_BG_COLOR, hover_color=UI_HOVER_COLOR,
                 on_click=None):
        super().__init__()
        self.__display_surface = pygame.display.get_surface()
        self.__font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        self.rect = pygame.Rect(x, y, width, height)
        self.__color = color
        self.__hover_color = hover_color
        self.__enabled = enabled

        self.__index = index
        self.__on_click = on_click
        self.__can_click = True
        self.__click_time = None
        self.__click_cooldown = 50  # para evitar que o usuário clique várias vezes sem querer

    def input(self):
        if self.__enabled:
            mouse_pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()
            if mouse[0] and self.rect.collidepoint(mouse_pos):
                self.__click_time = pygame.time.get_ticks()
                if self.__can_click:
                    self.__on_click(self.__index)
                    self.__can_click = False

    @abstractmethod
    def display(self):
        pass

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.__can_click and current_time - self.__click_time >= self.__click_cooldown:
            self.__can_click = True

    def button_update(self):
        self.cooldown()
        self.input()
        self.display()

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, index):
        self.__index = index

    @property
    def enabled(self):
        return self.__enabled

    @enabled.setter
    def enabled(self, enabled):
        self.__enabled = enabled

    @property
    def color(self):
        return self.__color

    @property
    def hover_color(self):
        return self.__hover_color

    @property
    def display_surface(self):
        return self.__display_surface

    @property
    def font(self):
        return self.__font


class UpgradeButton(Button):
    def __init__(self, x, y, index, on_click):
        super().__init__(x, y, 576, 128, index=index, on_click=on_click)

    def display(self):
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
            name_surf = self.font.render(self.index[1].name, False, TEXT_COLOR)
            name_rect = name_surf.get_rect(topleft=(self.rect.left + 10, self.rect.top + 10))
            self.display_surface.blit(name_surf, name_rect)
            # linha pra separar
            separator = pygame.Rect(name_rect.left, name_rect.bottom + 5, self.rect.width - 20, 4)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, separator)
            # ícone
            icon = self.index[1].icon
            icon_rect = icon.get_rect(topleft=(name_rect.left, separator.bottom + 10))
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR_ACTIVE, icon_rect, 4)
            self.display_surface.blit(icon, icon_rect)
            # descrição
            description_surf = pygame.Surface((482, 64)).convert_alpha()
            description_surf.fill([0, 0, 0, 0])
            description_rect = name_surf.get_rect(topleft=(icon_rect.right + 10, icon_rect.top))
            # separar as linhas da descrição
            words = self.index[1].description.split(' ')
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
