import pygame

from entity import Entity
from utils import load_sprite


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups, 'enemy')

        self.image = load_sprite('/test/enemy.png')

        self.rect = self.image.get_rect(topleft=pos)
        self._hitbox = self.rect.inflate(0, -26)
        self._obstacle_sprites = obstacle_sprites

        self._status = ''
        self._health = 3
        self._speed = 3
        self._collision_damage = 1
        self.__exp = 1

        # ataque
        self._damage_hitbox = self._hitbox.inflate(2, 2)  # hitbox maior que, quando colide com o player, dá dano nele
        self._can_attack = True
        self._attack_time = None
        self._attack_cooldown = 400

        # invencibilidade
        self._vulnerable = True
        self._hit_time = None
        self._invincibility_duration = 150

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
        if player.hitbox.colliderect(self._damage_hitbox) and self._can_attack:
            if self._status != 'attack':
                pass  # TODO: self.frame_index = 0
            self._status = 'attack'
        else:
            self._status = 'move'

    def actions(self, player):
        # faz uma ação baseado no status atual
        if self._status == 'attack':
            self._attack_time = pygame.time.get_ticks()
            self._can_attack = False  # TODO: passar para a lógica do animate() ao adicionar sprites
            player.damage(self._collision_damage)
        elif self._status == 'move':
            self._direction = self.get_player_distance_direction(player)[1]
        else:
            self._direction = pygame.math.Vector2()

    def animate(self):
        if not self._vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self._can_attack:
            if current_time - self._attack_time >= self._attack_cooldown:
                self._can_attack = True

        if not self._vulnerable:
            if current_time - self._hit_time >= self._invincibility_duration:
                self._vulnerable = True

    def damage(self, damage, player):
        if self._vulnerable:
            self._direction = self.get_player_distance_direction(player)[1]
            self._health -= damage
            self._hit_time = pygame.time.get_ticks()
            self._vulnerable = False

    def check_death(self, player):
        if self._health <= 0:
            self.kill()
            player.give_exp(self.__exp)

    def hit_reaction(self):
        if not self._vulnerable:
            self._direction = pygame.math.Vector2()  # fazer o inimigo parar ao tomar um ataque

    def move(self, speed, collision_hitbox_name='hitbox'):
        # o move() está sendo reescrito somente para atualizar a posição do damage_hitbox
        super().move(speed, collision_hitbox_name)
        self._damage_hitbox.center = self._hitbox.center

    def update(self):
        self.hit_reaction()
        self.move(self._speed)
        self.animate()
        self.cooldowns()

    def enemy_update(self, player):
        # esse enemy_update() é diferente do update() por receber o parâmetro player
        # ele também é chamado dentro do Level, mas, por ter uma assinatura diferente do update()
        # dos outros sprites, não pode ser chamado da mesma forma que eles
        self.check_death(player)
        self.get_status(player)
        self.actions(player)

    @property
    def obstacle_sprites(self):
        return self._obstacle_sprites

    @obstacle_sprites.setter
    def obstacle_sprites(self, obstacle_sprites):
        self._obstacle_sprites = obstacle_sprites

    @property
    def hitbox(self):
        return self._hitbox

    @property
    def collision_damage(self):
        return self._collision_damage

    @property
    def health(self):
        return self._health

    @property
    def vulnerable(self):
        return self._vulnerable
