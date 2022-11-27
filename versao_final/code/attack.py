import math
import pygame
import random
from abc import ABC, abstractmethod

from code.damage_area import EnemyDamageArea
from code.particles import FireSource, LightSource
from code.resources import Resources
from code.settings import WHITE


class Attack(ABC):
    def __init__(self, icon, attack_groups, obstacle_sprites, damage=1, cooldown=0, cast_sound='', hit_sound=''):
        self.__icon = Resources().get_sprite(icon)

        self.__attack_groups = attack_groups
        self.__obstacle_sprites = obstacle_sprites

        self.__base_damage = damage
        self.__damage = damage

        self.__base_cooldown = cooldown
        self.__cooldown = cooldown
        self.__can_attack = True
        self.__attack_time = 0

        if cast_sound != '':
            self.__cast_sound = Resources().get_sound(cast_sound)
        if hit_sound != '':
            self.__hit_sound = Resources().get_sound(hit_sound)

    @property
    def icon(self):
        return self.__icon

    def use(self, player, key):
        if self.__can_attack and key:
            player.staff.toggle_animation()
            self.create(player)
            self.block()

    def block(self):
        self.__can_attack = False
        self.__attack_time = self.__cooldown

    def check_cooldown(self):
        if not self.__can_attack:
            self.__attack_time -= 1
            if self.__attack_time <= 0:
                self.__can_attack = True

    @abstractmethod
    def create(self, player):
        pass

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, damage):
        self.__damage = damage

    @property
    def base_damage(self):
        return self.__base_damage

    @property
    def attack_groups(self):
        return self.__attack_groups

    @property
    def can_attack(self):
        return self.__can_attack

    @property
    def attack_time(self):
        return self.__attack_time

    @property
    def cooldown(self):
        return self.__cooldown

    @cooldown.setter
    def cooldown(self, cooldown):
        self.__cooldown = cooldown

    @property
    def base_cooldown(self):
        return self.__base_cooldown

    @property
    def cast_sound(self):
        return self.__cast_sound

    @property
    def hit_sound(self):
        return self.__hit_sound

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def attack_groups(self):
        return self.__attack_groups


class FireballAttack(Attack):
    def __init__(self, attack_groups, obstacle_sprites):
        super().__init__('/icons/fireball_attack.png', attack_groups, obstacle_sprites, damage=1, cooldown=75,
                         cast_sound='fireball_cast.ogg', hit_sound='fireball_hit.ogg')
        self.cast_sound.set_volume(0.2)
        self.hit_sound.set_volume(0.1)

    def create(self, player):
        pos = (player.staff.rect.x, player.staff.rect.y)
        sprite = Resources().get_sprite('/attacks/fireball.png')
        # calcular direção do projétil
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(pos[1] - mouse_pos[1], pos[0] - mouse_pos[0])
        direction = pygame.math.Vector2(-math.cos(angle), -math.sin(angle))
        # criar o projétil
        EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, damage=self.damage, speed=40,
                        direction=direction,
                        destroy_on_impact=True,
                        surface=sprite,
                        particle_spawners=[LightSource(pos, self.attack_groups[0]),
                                           FireSource(pos, self.attack_groups[0])],
                        hit_sound=self.hit_sound)
        self.cast_sound.play()


class SliceAttack(Attack):
    def __init__(self, attack_groups, obstacle_sprites):
        super().__init__('/icons/slice_attack.png', attack_groups, obstacle_sprites, damage=100, cooldown=120,
                         cast_sound='slice_cast.ogg', hit_sound='slice_hit.ogg')
        self.image = Resources().get_sprite('/test/slice.png')
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
            damage_area = EnemyDamageArea(current_pos, self.attack_groups, self.obstacle_sprites, damage=self.damage,
                                          surface=self.image, destroy_time=8, damage_time=1, hit_sound=self.hit_sound,
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


class AreaAttack(Attack):
    def __init__(self, attack_groups, obstacle_sprites):
        super().__init__('/icons/area_attack.png', attack_groups, obstacle_sprites, damage=100, cooldown=240,
                         cast_sound='area_cast.ogg')
        self.cast_sound.set_volume(0.5)

        self.__display_surface = pygame.display.get_surface()
        self.__attack_started = False

    def create(self, player):
        self.cast_sound.play()
        # pegar a posição do mouse 
        pos = pygame.mouse.get_pos()
        sprite = Resources().get_sprite('/test/area.png').copy()
        # criar o ataque
        damage_area = EnemyDamageArea(pos, self.attack_groups, self.obstacle_sprites, damage=self.damage,
                                      surface=sprite, destroy_time=60, damage_time=1, fade_out_step=4.25)
        damage_area.rect = sprite.get_rect(center=pos)
        # criar partículas
        particle_spawner = FireSource((player.staff.rect.centerx, player.staff.rect.y + 15), self.attack_groups[0])
        for i in range(5, 15):
            particle_spawner.offset = random.randint(16, 32)
            particle_spawner.update()
        particle_spawner.kill()

    def use(self, player, key):
        # reescrever o use para mostrar a área de dano enquanto o jogador está segurando Q
        # e só atacar ao soltar
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
                    self.create(player)
                    self.block()
                    self.__attack_started = False
