import pygame

from code.Entity import Entity
from code.GroupManager import GroupManager
from code.Settings import *

class PlayerDamageArea(Entity):
    def __init__(self, pos, damage=0, speed=0, direction=pygame.math.Vector2, 
                 surface=pygame.Surface((TILESIZE, TILESIZE)), destroy_time=60,
                 particle_spawners=[], hit_sound=None, fade_out_step=0) -> None:
        super().__init__('player_damage_area')
        self.__group_manager = GroupManager()
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
        player = self.group_manager.player
        collision = player.hitbox.colliderect(self.__hitbox)
        if collision and player.vulnerable:
            # dar o dano no player
            player.damage(self.__damage) 

            try: # tocar o som de hit
                # evitar exceção caso o arquivo de som não exista
                self.hit_sound.play() 
            except Exception:
                pass
            
            # destruir o ataque
            self.kill()

    def update(self):
        self.player_collision()

        moved = self.move(self.speed, 'smaller_hitbox')
        if not moved:
            # projétil colidiu com algum obstáculo
            self.kill()

        for particle_spawner in self.__particle_spawners:
            particle_spawner.rect.center = self.rect.center + self.direction * self.speed

        self.__destroy_timer += 1
        if self.__destroy_timer >= self.__destroy_time:
            self.kill()
        
    @property
    def speed(self):
        return self.__speed

    @property
    def group_manager(self):
        return self.__group_manager

    @property
    def hit_sound(self):
        return self.__hit_sound

    @property
    def hitbox(self):
        return self.__hitbox

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def damage(self):
        return self.__damage