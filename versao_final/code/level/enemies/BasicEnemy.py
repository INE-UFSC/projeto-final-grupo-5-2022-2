import pygame

from code.level.Entity import Entity
from code.level.GroupManager import GroupManager
from code.library.Resources import Resources
from code.level.enemies.EnemyStatus import Melee_Status


class Enemy(Entity):
    def __init__(self, name, pos, health=1, speed=3, collision_damage=1, exp=1,
                 attack_cooldown=40):
        super().__init__('enemy')

        self.__group_manager = GroupManager()
        self.__name = name

        self.__animation = Resources().get_animation(f'/enemies/{name}/move')
        self.__frame_index = 0
        self.__animation_speed = 0.2
        self.image = self.__animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.inflate(0, - self.image.get_height() // 1.5)
        self.__hitbox.bottom = self.rect.bottom
        self.__obstacle_sprites = self.__group_manager.enemy_obstacle_sprites

        self.__status = Melee_Status.MOVE
        self.__health = health
        self.__speed = speed
        self.__collision_damage = collision_damage
        self.__exp = exp

        # ataque
        self.__damage_hitbox = self.__hitbox.inflate(2, 2)  # hitbox maior que, quando colide com o player, dá dano nele
        self.__can_attack = True
        self.__attack_time = 0
        self.__attack_cooldown = attack_cooldown

        # invencibilidade
        self.__vulnerable = True
        self.__hit_time = 0
        self.__invincibility_duration = 20

    def get_player_distance_direction(self):
        # TODO: dividir esse método
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player = self.__group_manager.player
        player_vec = pygame.math.Vector2(player.rect.center)
        sub_vec = player_vec - enemy_vec
        distance = sub_vec.magnitude()

        if distance > 0:
            direction = sub_vec.normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self):
        # decide o status atual
        player = self.__group_manager.player
        if player.hitbox.colliderect(self.__damage_hitbox) and self.__can_attack:
            if self.__status != Melee_Status.ATTACK:
                pass  # TODO: self.frame_index = 0
            self.__status = Melee_Status.ATTACK
        else:
            self.__status = Melee_Status.MOVE

    def actions(self):
        # faz uma ação baseado no status atual
        player = self.__group_manager.player
        if self.__status == Melee_Status.ATTACK:
            self.__attack_time = self.__attack_cooldown
            self.__can_attack = False  # TODO: passar para a lógica do animate() ao adicionar sprites
            player.damage(self.__collision_damage)
        elif self.__status == Melee_Status.MOVE:
            self.direction = self.get_player_distance_direction()[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        player = self.__group_manager.player
        self.__frame_index += self.__animation_speed
        if self.__frame_index >= len(self.__animation):
            self.__frame_index = 0
        self.image = self.__animation[int(self.__frame_index)]
        if player.hitbox.x < self.__hitbox.x:
            # virar o inimigo em direção do player
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center=self.hitbox.center)
        # animação de vulnerabilidade
        if not self.__vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        if not self.__can_attack:
            self.__attack_time -= 1
            if self.__attack_time <= 0:
                self.__can_attack = True

        if not self.__vulnerable:
            self.__hit_time -= 1
            if self.__hit_time <= 0:
                self.__vulnerable = True

    def damage(self, damage):
        if self.__vulnerable:
            self.direction = self.get_player_distance_direction()[1]
            self.__health -= damage
            self.__hit_time = self.__invincibility_duration
            self.__vulnerable = False

    def check_death(self):
        if self.__health <= 0:
            player = self.__group_manager.player
            player.give_exp(self.__exp)
            self.kill()

    def hit_reaction(self):
        if not self.__vulnerable:
            self.direction = pygame.math.Vector2()  # fazer o inimigo parar ao tomar um ataque

    def move(self, speed, collision_hitbox_name='hitbox'):
        # o move() está sendo reescrito somente para atualizar a posição do damage_hitbox
        super().move(speed, collision_hitbox_name)
        self.__damage_hitbox.center = self.__hitbox.center

    def update(self):
        self.__obstacle_sprites = GroupManager().enemy_obstacle_sprites
        self.hit_reaction()
        self.move(self.__speed)
        self.cooldowns()
        self.check_death()
        self.get_status()
        self.actions()
        self.animate()

    @property
    def group_manager(self):
        return self.__group_manager

    @property
    def name(self):
        return self.__name

    @property
    def obstacle_sprites(self):
        return self.__obstacle_sprites

    @obstacle_sprites.setter
    def obstacle_sprites(self, obstacle_sprites):
        self.__obstacle_sprites = obstacle_sprites

    @property
    def hitbox(self):
        return self.__hitbox

    @property
    def collision_damage(self):
        return self.__collision_damage

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, health):
        self.__health = health

    @property
    def vulnerable(self):
        return self.__vulnerable

    @vulnerable.setter
    def vulnerable(self, vulnerable):
        self.__vulnerable = vulnerable

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        self.__status = status

    @property
    def speed(self):
        return self.__speed

    @property
    def exp(self):
        return self.__exp

    @property
    def damage_hitbox(self):
        return self.__damage_hitbox

    @property
    def can_attack(self):
        return self.__can_attack

    @can_attack.setter
    def can_attack(self, can_attack):
        self.__can_attack = can_attack

    @property
    def attack_time(self):
        return self.__attack_time

    @attack_time.setter
    def attack_time(self, attack_time):
        self.__attack_time = attack_time

    @property
    def attack_cooldown(self):
        return self.__attack_cooldown

    @attack_cooldown.setter
    def attack_cooldown(self, attack_cooldown):
        self.__attack_cooldown = attack_cooldown

    @property
    def hit_time(self):
        return self.__hit_time

    @property
    def invincibility_duration(self):
        return self.__invincibility_duration

    @property
    def frame_index(self):
        return self.__frame_index

    @frame_index.setter
    def frame_index(self, frame_index):
        self.__frame_index = frame_index

    @property
    def animation(self):
        return self.__animation

    @animation.setter
    def animation(self, animation):
        self.__animation = animation

    @property
    def animation_speed(self):
        return self.__animation_speed
