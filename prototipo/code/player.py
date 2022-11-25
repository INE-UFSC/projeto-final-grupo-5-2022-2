import sys

from code.attack import *
from code.entity import Entity


class Player(Entity):
    def __init__(self, groups, attack_groups, obstacle_sprites):
        super().__init__(groups, 'player')
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

        self.__health = 3
        self.__max_health = 7
        self.__base_speed = 5
        self.__move_speed = self.__base_speed

        self.__exp = 0
        self.__level_up_exp = 10
        self.__level_up_exp_increment = 10
        self.__current_level = 1
        self.__upgrade_points = 0
        self.__upgrade_list = []

        # movimento
        self.__obstacle_sprites = obstacle_sprites
        self.__speed = 5

        # ataques
        self.__attacks = [FireballAttack(attack_groups, obstacle_sprites),
                          SliceAttack(attack_groups, obstacle_sprites),
                          AreaAttack(attack_groups, obstacle_sprites)]

        # dano
        self.__vulnerable = True
        self.__hurt_time = 0
        self.__invincibility_duration = 60

        # cajado (somente desenha o sprite)
        self.__staff = Staff(groups)

    def input(self):
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
            attack.use(self, attack_keys[i])

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
        if self.__vulnerable:
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
            upgrade.apply(self)
            self.__upgrade_list.append(upgrade)

    def give_health(self, health):
        self.__health += health
        if self.__health > self.__max_health:
            self.__health = self.__max_health

    def check_death(self):
        if self.__health <= 0:
            # TEMPORÁRIO
            # futuramente, é necessário implementar a tela de GAME OVER
            pygame.quit()
            sys.exit()

    def update(self):
        self.check_death()
        self.input()
        self.animate()
        self.staff.animate(self)
        self.move(self.__move_speed)
        self.cooldowns()

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
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @obstacle_sprites.setter
    def obstacle_sprites(self, obstacle_sprites):
        self.__obstacle_sprites = obstacle_sprites

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
    def level_ip_ex_increment(self):
        return self.__level_up_exp_increment


class Staff(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.__sprite_type = 'staff'
        self.__animation = Resources().get_animation('/staff')
        self.__frame_index = 0
        self.__animation_speed = 0.2
        self.__animate = False
        self.image = self.__animation[0]
        self.rect = self.image.get_rect()
        self.__original_rect = self.rect

    @property
    def sprite_type(self):
        return self.__sprite_type

    def toggle_animation(self):
        self.__animate = True
        self.__light = LightSource(self.rect.center, self.groups())

    def animate(self, player):
        if self.__animate:
            self.__light.rect.center = self.rect.center
            self.__frame_index += self.__animation_speed
            if self.__frame_index >= len(self.__animation):
                self.__frame_index = 0
                self.__animate = False
                self.__light.kill()
        else:
            self.__frame_index = 1 - self.__animation_speed
        self.image = self.__animation[int(self.__frame_index)]
        self.rect.center = player.rect.center + pygame.math.Vector2(20, -10)
        # atualizar posição do cajado
        mouse_pos = pygame.mouse.get_pos()
        dist = math.sqrt(
            (mouse_pos[0] - player.rect.centerx) ** 2 + (mouse_pos[1] - player.rect.centery) ** 2)
        angle = math.atan2(player.rect.centery - mouse_pos[1], player.rect.centerx - mouse_pos[0])
        sin = -math.sin(angle)
        cos = -math.cos(angle)
        offset = (dist // 32) ** 1 / 2
        self.rect.center = self.__original_rect.center + pygame.Vector2(cos * offset, sin * offset)
