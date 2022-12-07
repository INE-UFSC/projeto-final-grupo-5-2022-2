import math

import pygame

from code.damage.EnemyDamageArea import EnemyDamageArea
from code.GroupManager import GroupManager
from code.Resources import Resources
from code.attacks.Attack import Attack


class SliceAttack(Attack):
    def __init__(self):
        super().__init__('/icons/slice_attack.png', damage=100, cooldown=120,
                         cast_sound='slice_cast.ogg', hit_sound='slice_hit.ogg')
        self.image = Resources().get_sprite('/test/slice.png')
        self.cast_sound.set_volume(0.1)
        self.hit_sound.set_volume(0.1)

    def create(self):
        # essa função basicamente vai criando damage areas a cada intervalo
        # 'step' em direção do mouse até chegar nele ou o sprite colidir em uma parede
        # no final, ele move o sprite do player para a última posição com uma damage area
        # desde que o player não colida com uma parede
        player = GroupManager().player
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
            damage_area = EnemyDamageArea(current_pos, damage=self.damage,
                                          surface=self.image, destroy_time=8, damage_time=1, hit_sound=self.hit_sound,
                                          blood_on_kill=True,
                                          screen_shake_on_kill=True,
                                          direction=direction)
            damage_area.rect.center = current_pos
            self.group_manager.add_to_attacks(damage_area)

            # condições para parar de criar
            for obstacle in GroupManager().tile_sprites:
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
            for sprite in GroupManager().tile_sprites:
                if player.hitbox.colliderect(sprite.hitbox):
                    pos_list.pop()
                    break
            else:
                # se colidiu com algo, o for deu break e esse while consequentemente vai dar break
                # sem posicionar o player
                break
            player.hitbox.center = pos_list.pop()
            # caso não sobre posições na lista, o player vai permanecer na posição inicial
