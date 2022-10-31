import math
from abc import ABC, abstractmethod

import pygame.transform

from damage_area import EnemyDamageArea
from particles import FireSource, LightSource
from utils import *


class Attack(ABC):
    def __init__(self, icon, attack_groups, obstacle_sprites, cooldown=0, cast_sound='', hit_sound=''):
        self.icon = load_sprite(icon)

        self.attack_groups = attack_groups
        self.obstacle_sprites = obstacle_sprites

        self.cooldown = cooldown
        self.can_attack = True
        self.attack_time = 0

        if cast_sound != '':
            self.cast_sound = load_sound(cast_sound)
        if hit_sound != '':
            self.hit_sound = load_sound(hit_sound)

    def use(self, player):
        if self.can_attack:
            self.create(player)
            self.block()

    def block(self):
        self.can_attack = False
        self.attack_time = pygame.time.get_ticks()

    def check_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack and current_time - self.attack_time >= self.cooldown:
            self.can_attack = True

    @abstractmethod
    def create(self, player):
        pass


class FireballAttack(Attack):
    def __init__(self, attack_groups, obstacle_sprites):
        super().__init__(os.path.join('test','icon_fireball.png'), attack_groups, obstacle_sprites, cooldown=900,
                         cast_sound='fireball_cast.ogg', hit_sound='fireball_hit.ogg')
        self.cast_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.1)

    def create(self, player):
        pos = (player.staff.rect.x, player.staff.rect.y)
        sprite = load_sprite(os.path.join('test', 'fireball.png'))
        # calcular direção do projétil
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[1] - mouse_pos[1], pos[0] - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # criar o projétil
        EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, damage=1, speed=40, direction=direction,
                        destroy_on_impact=True,
                        surface=sprite,
                        particle_spawners=[LightSource(pos, self.attack_groups[0]),
                                           FireSource(pos, self.attack_groups[0])],
                        hit_sound=self.hit_sound)
        self.cast_sound.play()


class LineAttack(Attack):
    def __init__(self, attack_groups, obstacle_sprites):
        super().__init__(os.path.join('test','icon_line.png'), attack_groups, obstacle_sprites, cooldown=2400)

    def create(self, player):
        pos = (player.staff.rect.centerx, player.staff.rect.y + 12)
        sprite = load_sprite(os.path.join('test', 'kamehameha.png'))
        pivot = (0, 12)
        # rotacionar o sprite
        mouse_pos = pygame.mouse.get_pos()
        angle = 360 - math.degrees(math.atan2(mouse_pos[1] - pos[1], mouse_pos[0] - pos[0]))
        image_rect = sprite.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        sprite = pygame.transform.rotate(sprite, angle)
        sprite_rect = sprite.get_rect(center=rotated_image_center)
        # criar o ataque
        damage_area = EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, damage=5, surface=sprite,
                                      destroy_time=180)
        damage_area.rect = sprite_rect


class SliceAttack(Attack):
    def __init__(self, attack_groups, obstacle_sprites):
        super().__init__(os.path.join('test', 'icon_slice.png'), attack_groups, obstacle_sprites, cooldown=1200,
                         cast_sound='slice_cast.ogg', hit_sound='slice_hit.ogg')
        self.image = load_sprite(os.path.join('test', 'slice.png'))
        self.cast_sound.set_volume(0.1)
        self.hit_sound.set_volume(0.1)

    def create(self, player):
        # essa função basicamente vai criando damage areas a cada intervalo
        # 'step' em direção do mouse até chegar nele ou o sprite colidir em uma parede
        # no final, ele move o sprite do player para a última posição com uma damage area
        # desde que o player não colida com uma parede
        self.cast_sound.play()
        current_pos = player.hitbox.center
        # calcular direção do corte
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(current_pos[1] - mouse_pos[1], current_pos[0] - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # calcular a posição da linha
        step = 16  # de quantos em quantos pixels a damage area vai andar
        pos_list = [current_pos]
        # condições para sair do while
        x_relation = mouse_pos[0] > current_pos[0]
        y_relation = mouse_pos[1] > current_pos[1]
        collided = False
        while True:
            # criar o próximo damage area
            current_pos = (current_pos[0] + direction.x * step, current_pos[1] + direction.y * step)
            pos_list.append(current_pos)
            damage_area = EnemyDamageArea(current_pos, self.attack_groups, self.obstacle_sprites, damage=5,
                                          surface=self.image, destroy_time=100, hit_sound=self.hit_sound,
                                          blood_on_kill=True,
                                          direction=direction)
            damage_area.rect.center = current_pos

            # condições para parar de criar
            for obstacle in self.obstacle_sprites:
                if damage_area.rect.colliderect(obstacle.rect):
                    collided = True
                    break
            if collided:
                break

            new_x_relation = mouse_pos[0] > current_pos[0]
            new_y_relation = mouse_pos[1] > current_pos[1]
            if new_y_relation != y_relation or new_x_relation != x_relation:
                break

        # posicionar o player
        while len(pos_list) > 0:
            # esse loop vai removendo todas as posições em que o player colidiria com uma parede
            player.hitbox.center = pos_list[len(pos_list) - 1]
            for sprite in self.obstacle_sprites:
                if player.hitbox.colliderect(sprite.hitbox):
                    pos_list.pop()
                    break
            else:
                # se colidiu com algo, o for deu break e esse while consequentemente vai dar break
                # sem posicionar o player
                break
            player.hitbox.center = pos_list.pop()
            # caso não sobre posições na lista, o player vai permanecer na posição inicial
