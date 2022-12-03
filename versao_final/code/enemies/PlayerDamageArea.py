import pygame

from code.entity import Entity
from code.group_manager import GroupManager
from code.settings import *

class PlayerDamageArea(Entity):
    def __init__(self, pos, damage=0, speed=0, direction=pygame.math.Vector2, 
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=60,
                 particle_spawners=[], hit_sound=None, fade_out_step=0) -> None:
        super().__init__('player_damage_area')
        self.__group_manager = GroupManager()
        self.__group_manager.add_to_enemy_attacks(self)
        self.image = surface
        self.rect = self.image.get_rect(center=pos)
        self.__hitbox = self.rect

        self.__damage = damage
        self.__speed = speed
        self.direction = direction
        self.__obstacle_sprites = self.__group_manager.tile_sprites
        self.__particle_spawners = particle_spawners

        self.__destroy_time = destroy_time
        self.__destroy_timer = 0
        self.__fade_out_step = fade_out_step

        self.__hit_sound = hit_sound

    def player_collision(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.__group_manager.player, False)
        if collision_sprites:
            player = collision_sprites[0]
            if player.vulnerable:
                # dar o dano no player
                player.damage(self.__damage) 

                try: # tocar o som de hit
                    # evitar exceção caso o arquivo de som não exista
                    self.__hit_sound.play() 
                except Exception:
                    pass
                
                # destruir o ataque
                self.kill

    def update(self):
        pass