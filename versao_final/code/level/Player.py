import pygame

from code.level.Entity import Entity
from code.level.GroupManager import GroupManager
from code.level.Staff import Staff
from code.level.attacks.AreaAttack import AreaAttack
from code.level.attacks.FireballAttack import FireballAttack
from code.level.attacks.SliceAttack import SliceAttack
from code.library.Resources import Resources
from code.save.PlayerDAO import PlayerDAO

class Player(Entity):
    def __init__(self):
        self.__staff = Staff()  # cajado (somente desenha o sprite)
        super().__init__('player')
        self.__group_manager = GroupManager()
        self.__player_dao = PlayerDAO()

        # importar animações
        self.__animations = {'up': [], 'down': [], 'left': [], 'right': []}
        for animation in self.__animations.keys():
            self.__animations[animation] = Resources().get_animation(f'/player/{animation}')
        self.__state = 'down'
        self.__frame_index = 0
        self.__animation_speed = 0.2

        self.image = self.__animations['down'][0]
        self.rect = self.image.get_rect(topleft=(300, 300))
        self.__hitbox = self.rect.inflate(-16, -26)

        self.__health = 7
        self.__max_health = 7
        self.__base_speed = 5
        self.__move_speed = self.__base_speed

        self.__exp = 0
        self.__level_up_exp = 10
        self.__level_up_exp_increment = 0
        self.__current_level = 1
        self.__upgrade_points = 0
        self.__upgrade_list = []

        # movimento
        self.__obstacle_sprites = self.__group_manager.player_obstacle_sprites
        self.__speed = 5
        self.__ignore_input = False

        # ataques
        self.__attacks = [FireballAttack(), SliceAttack(), AreaAttack()]

        # dano
        self.__vulnerable = True
        self.__hurt_time = 0
        self.__invincibility_duration = 60

    def input(self):
        # ignorar input caso o player esteja morto ou em transição
        if self.ignore_input:
            return

        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # movimento vertical
        if keys[pygame.K_w]:
            self.direction.y = -1
            self.__state = 'up'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.__state = 'down'
        else:
            self.direction.y = 0
        # movimento horizontal
        if keys[pygame.K_d]:
            self.direction.x = 1
            self.__state = 'right'
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.__state = 'left'
        else:
            self.direction.x = 0

        # ataques
        attack_keys = (mouse[0], mouse[2], keys[pygame.K_q])
        for i, attack in enumerate(self.__attacks):
            attack.use(attack_keys[i])

    def cooldowns(self):
        for attack in self.__attacks:
            attack.check_cooldown()

        if not self.__vulnerable:
            self.__hurt_time -= 1
            if self.__hurt_time <= 0:
                self.__vulnerable = True

    def animate(self):
        animation = self.__animations[self.__state]
        if self.direction.x == 0 and self.direction.y == 0:
            self.__frame_index = 1 - self.__animation_speed
            # para reproduzir o próximo frame instantaneamente após
            # começar a mover
        else:
            self.__frame_index += self.__animation_speed
            if self.__frame_index >= len(animation):
                self.__frame_index = 0
        self.image = animation[int(self.__frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        # animação de vulnerabilidade
        if not self.__vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def damage(self, damage):
        if self.vulnerable and damage > 0:
            self.__health -= damage
            self.__vulnerable = False
            self.__hurt_time = self.__invincibility_duration

    def give_exp(self, exp):
        self.__exp += exp
        while self.__exp >= self.__level_up_exp:
            self.__exp -= self.__level_up_exp
            self.__current_level += 1
            self.__upgrade_points += 1
            self.__level_up_exp += self.__level_up_exp_increment

    def give_upgrade(self, upgrade):
        if self.__upgrade_points > 0:
            self.__upgrade_points -= 1
            upgrade.apply()
            self.__upgrade_list.append(upgrade)

    def give_health(self, health):
        self.__health += health
        if self.__health > self.__max_health:
            self.__health = self.__max_health

    def update(self):
        if self.is_dead:
            return

        self.__obstacle_sprites = self.__group_manager.player_obstacle_sprites
        self.input()
        self.animate()
        self.__staff.animate(self)
        self.move(self.__move_speed)
        self.cooldowns()

    def save(self):
        save_data = {
            'level': self.__current_level,
            'exp': self.__exp,
            'health': self.__health,
            'upgrades': self.__upgrade_list
        }
        for key in save_data:
            self.__player_dao.add(key, save_data[key])
    
    def load_save(self):
        save_data = self.__player_dao.get_all()
        self.__current_level = save_data['level']
        self.__exp = save_data['exp']
        self.__health = save_data['health']
        self.__upgrade_list = save_data['upgrades']
        for upgrade in self.__upgrade_list:
            upgrade.apply()

    @property
    def is_dead(self):
        return self.__health <= 0

    @property
    def player_dao(self):
        return self.__player_daos

    @property
    def hitbox(self):
        return self.__hitbox

    @hitbox.setter
    def hitbox(self, hitbox):
        self.__hitbox = hitbox

    @property
    def attacks(self):
        return self.__attacks

    @property
    def health(self):
        return self.__health

    @property
    def max_health(self):
        return self.__max_health

    @property
    def move_speed(self):
        return self.__move_speed

    @move_speed.setter
    def move_speed(self, speed):
        self.__move_speed = speed

    @property
    def base_speed(self):
        return self.__base_speed

    @property
    def exp(self):
        return self.__exp

    @property
    def vulnerable(self):
        return self.__vulnerable

    @property
    def staff(self):
        return self.__staff

    @property
    def level_up_exp(self):
        return self.__level_up_exp

    @property
    def current_level(self):
        return self.__current_level

    @property
    def upgrade_points(self):
        return self.__upgrade_points

    @property
    def speed(self):
        return self.__speed

    @speed.setter
    def speed(self, speed):
        self.__speed = speed

    @property
    def upgrade_list(self):
        return self.__upgrade_list

    @property
    def level_up_exp_increment(self):
        return self.__level_up_exp_increment

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @property
    def ignore_input(self):
        return self.__ignore_input

    @ignore_input.setter
    def ignore_input(self, ignore):
        self.__ignore_input = ignore
