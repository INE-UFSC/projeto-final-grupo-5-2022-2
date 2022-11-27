import pygame

from code.entity import Entity
from code.resources import Resources


class Enemy(Entity):
    def __init__(self, name, pos, groups, obstacle_sprites, health=1, speed=3, collision_damage=1, exp=1,
                 attack_cooldown=40):
        super().__init__(groups, 'enemy')
        self.__animation = Resources().get_animation(f'/enemies/{name}')
        self.__frame_index = 0
        self.__animation_speed = 0.2
        self.image = self.__animation[0]
        self.rect = self.image.get_rect(topleft=pos)
        self.__hitbox = self.rect.inflate(0, - self.image.get_width() // 5)
        self.__obstacle_sprites = obstacle_sprites

        self.__status = ''
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

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        sub_vec = player_vec - enemy_vec
        distance = sub_vec.magnitude()

        if distance > 0:
            direction = sub_vec.normalize()
        else:
            direction = pygame.math.Vector2()

        return distance, direction

    def get_status(self, player):
        # decide o status atual
        if player.hitbox.colliderect(self.__damage_hitbox) and self.__can_attack:
            if self.__status != 'attack':
                pass  # TODO: self.frame_index = 0
            self.__status = 'attack'
        else:
            self.__status = 'move'

    def actions(self, player):
        # faz uma ação baseado no status atual
        if self.__status == 'attack':
            self.__attack_time = self.__attack_cooldown
            self.__can_attack = False  # TODO: passar para a lógica do animate() ao adicionar sprites
            player.damage(self.__collision_damage)
        elif self.__status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self, player):
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

    def damage(self, damage, player):
        if self.__vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.__health -= damage
            self.__hit_time = self.__invincibility_duration
            self.__vulnerable = False

    def check_death(self, player):
        if self.__health <= 0:
            self.kill()
            player.give_exp(self.__exp)

    def hit_reaction(self):
        if not self.__vulnerable:
            self.direction = pygame.math.Vector2()  # fazer o inimigo parar ao tomar um ataque

    def move(self, speed, collision_hitbox_name='hitbox'):
        # o move() está sendo reescrito somente para atualizar a posição do damage_hitbox
        super().move(speed, collision_hitbox_name)
        self.__damage_hitbox.center = self.__hitbox.center

    def update(self):
        self.hit_reaction()
        self.move(self.__speed)
        self.cooldowns()

    def enemy_update(self, player):
        # esse enemy_update() é diferente do update() por receber o parâmetro player
        # ele também é chamado dentro do Level, mas, por ter uma assinatura diferente do update()
        # dos outros sprites, não pode ser chamado da mesma forma que eles
        self.check_death(player)
        self.get_status(player)
        self.actions(player)
        self.animate(player)

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

    @property
    def attack_time(self):
        return self.__attack_time

    @property
    def attack_cooldown(self):
        return self.__attack_cooldown

    @property
    def hit_time(self):
        return self.__hit_time

    @property
    def invincibility_duration(self):
        return self.__invincibility_duration
