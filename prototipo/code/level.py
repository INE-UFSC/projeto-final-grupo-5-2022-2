import pygame.math

from enemy import Enemy
from particles import *
from player import Player
from settings import *
from tile import Tile
from ui import UI


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        # sprites
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        # criar o mapa
        self.create_map()

        self.ui = UI()

        self.timer = 0  # TEMPORÁRIO

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], [self.visible_sprites, self.attack_sprites],
                                         self.obstacle_sprites)
                elif col == 'e':
                    Enemy('test', (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites)

        # permite os inimigos colidirem com os outros inimigos e com o player
        enemy_obstacle_sprites = pygame.sprite.Group(self.player, self.obstacle_sprites, self.attackable_sprites)
        for sprite in self.attackable_sprites:
            sprite.obstacle_sprites = enemy_obstacle_sprites
        # permite o player colidir com os inimigos
        self.player.obstacle_sprites = pygame.sprite.Group(self.obstacle_sprites, self.attackable_sprites)

    def toggle_menu(self):
        self.ui.toggle_menu()

    def run(self):
        self.visible_sprites.custom_draw()
        self.ui.display(self.player)

        if not self.ui.is_menu_open:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            # conferir colisão dos ataques com os inimigos
            for attack_sprite in self.attack_sprites:
                attack_sprite.enemy_collision(self.player, self.attackable_sprites)
            # invocar inimigo (TEMPORÁRIO)
            self.timer += 1
            if self.timer % 120 == 0:
                Enemy('test', (320, 320), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.back_sprite_types = ['on_ground']
        self.front_sprite_types = ['light']

    def custom_draw(self):
        # separar os sprites que devem sempre ir atrás dos outros e sempre na frente
        # alguns sprites que necessariamente devem ir atrás são as partículas de sangue, que devem ficar
        # atrás de tudo por "estar no chão"
        # a maioria dos sprites fica no meio
        # um sprite que necessariamente deve ir na frente são as partículas de luz
        back_sprites = list(filter(lambda sprite: sprite.sprite_type in self.back_sprite_types, self.sprites()))
        middle_sprites = list(
            filter(lambda sprite: sprite.sprite_type not in self.back_sprite_types + self.front_sprite_types,
                   self.sprites()))
        front_sprites = list(filter(lambda sprite: sprite.sprite_type in self.front_sprite_types, self.sprites()))
        # desenhar os sprites na ordem
        sprite_lists = [back_sprites, middle_sprites, front_sprites]
        for sprite_list in sprite_lists:
            for sprite in sorted(sprite_list, key=lambda sprite: sprite.rect.centery):
                self.display_surface.blit(sprite.image, sprite.rect)

    def enemy_update(self, player):
        # os inimigos possuem um update() chamado enemy_update() que precisa receber o player como
        # parâmetro para algumas interações
        # essa função chama esse outro update()
        enemy_sprites = [sprite for sprite in self.sprites() if sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
