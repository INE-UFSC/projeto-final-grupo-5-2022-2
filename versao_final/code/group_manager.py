import pygame

from code.singleton import Singleton


class GroupManager(Singleton):
    def __init__(self) -> None:
        if not self._initialized:
            # sprites que são desenhados
            self.__visible_sprites = pygame.sprite.Group()
            # efeitos que são sobrepostos a todos os outros sprites
            self.__effects_sprites = pygame.sprite.Group()
            # player
            self.__player = None
            self.__player_sprites = pygame.sprite.Group()
            # sprites relacionados ao ataque
            self.__attack_sprites = pygame.sprite.Group()
            self.__enemy_sprites = pygame.sprite.Group()
            # sprites que funcionam como obstáculos
            self.__tile_sprites = pygame.sprite.Group()
            self.__enemy_obstacle_sprites = pygame.sprite.Group()
            self.__player_obstacle_sprites = pygame.sprite.Group()
            # partículas
            self.__particle_sprites = pygame.sprite.Group()

            self._initialized = True

    @property
    def player(self):
        return self.__player

    def add_to_attacks(self, sprite):
        self.__attack_sprites.add(sprite)
        self.__update_groups()

    def add_to_enemies(self, sprite):
        self.__enemy_sprites.add(sprite)
        self.__update_groups()

    def add_to_tiles(self, sprite):
        self.__tile_sprites.add(sprite)
        self.__update_groups()

    def add_to_particles(self, sprite):
        self.__particle_sprites.add(sprite)
        self.__update_groups()

    def __update_groups(self):
        self.__enemy_obstacle_sprites = pygame.sprite.Group(self.__tile_sprites, self.__enemy_sprites)
        self.__player_obstacle_sprites = self.__enemy_obstacle_sprites

        if self.__player:
            self.__enemy_obstacle_sprites.add(self.__player)
            self.__player_sprites = pygame.sprite.Group(self.__player)
            if self.__player.staff:
                self.__player_sprites.add(self.__player.staff)

        # sprites que serão desenhados
        self.__visible_sprites = pygame.sprite.Group(self.effects_sprites,
                                                     self.__player_sprites,
                                                     self.__tile_sprites,
                                                     self.__enemy_sprites,
                                                     self.__attack_sprites,
                                                     self.__particle_sprites)

    def clear_all(self):
        # limpa todos os grupos menos o player
        for attribute, value in self.__dict__.items():
            if isinstance(value, pygame.sprite.Group):
                value.empty()

    @property
    def player(self):
        return self.__player

    @player.setter
    def player(self, player):
        self.__player = player
        self.__update_groups()

    @property
    def visible_sprites(self):
        return self.__visible_sprites

    @property
    def effects_sprites(self):
        return self.__effects_sprites

    @property
    def attack_sprites(self):
        return self.__attack_sprites

    @property
    def enemy_sprites(self):
        return self.__enemy_sprites

    @property
    def tile_sprites(self):
        return self.__tile_sprites

    @property
    def enemy_obstacle_sprites(self):
        return self.__enemy_obstacle_sprites

    @property
    def player_obstacle_sprites(self):
        return self.__player_obstacle_sprites
