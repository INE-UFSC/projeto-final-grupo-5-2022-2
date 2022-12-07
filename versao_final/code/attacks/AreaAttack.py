import pygame
import random

from code.EnemyDamageArea import EnemyDamageArea
from code.GroupManager import GroupManager
from code.Particles import AnimationParticle, FireSource
from code.Resources import Resources
from code.Settings import WHITE
from code.attacks.Attack import Attack


class AreaAttack(Attack):
    def __init__(self):
        super().__init__('/icons/area_attack.png', damage=100, cooldown=240, cast_sound='area_cast.ogg')
        self.cast_sound.set_volume(0.5)

        self.__display_surface = pygame.display.get_surface()
        self.__attack_started = False

    def create(self):
        player = GroupManager().player
        self.cast_sound.play()
        # pegar a posição do mouse
        pos = pygame.mouse.get_pos()
        sprite = Resources().get_sprite('/test/area.png').copy()
        # criar o ataque
        damage_area = EnemyDamageArea(pos, damage=self.damage, surface=sprite, destroy_time=60, damage_time=1,
                                      fade_out_step=4.25)
        damage_area.sprite_type = 'on_ground'
        self.group_manager.add_to_attacks(damage_area)
        # criar partículas
        explosion_animation = Resources().get_animation('/attacks/explosion')
        explosion_pos = (damage_area.rect.centerx, damage_area.rect.centery - damage_area.image.get_height() // 2)
        explosion = AnimationParticle(explosion_pos, explosion_animation, 0.2, destroy_on_end=True)
        self.group_manager.add_to_particles(explosion)
        fire = FireSource((player.staff.rect.centerx, player.staff.rect.y + 15))
        self.group_manager.add_to_particles(fire)
        for i in range(5, 15):
            fire.offset = random.randint(16, 32)
            fire.update()
        fire.kill()

    def use(self, key):
        # reescrever o use para mostrar a área de dano enquanto o jogador está segurando Q
        # e só atacar ao soltar
        player = GroupManager().player
        if self.can_attack:
            if key:
                # desenhar o indicador de área
                self.__attack_started = True
                mouse_pos = pygame.mouse.get_pos()
                area_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], 256, 256)
                area_rect.center = mouse_pos
                pygame.draw.rect(self.__display_surface, WHITE, area_rect, 4)
            else:
                # criar o ataque
                if self.__attack_started:
                    player.staff.toggle_animation()
                    self.create()
                    self.block()
                    self.__attack_started = False
