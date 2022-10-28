import pygame

from entity import Entity
from utils import load_sprite


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups, 'enemy')

        self.image = load_sprite('/test/enemy.png')

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.obstacle_sprites = obstacle_sprites

        self.status = ''
        self.health = 3
        self.speed = 3
        self.collision_damage = 1

        # ataque
        self.damage_hitbox = self.hitbox.inflate(2, 2)  # hitbox maior que, quando colide com o player, dá dano nele
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400

        # invencibilidade
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 150

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
        if player.hitbox.colliderect(self.damage_hitbox) and self.can_attack:
            if self.status != 'attack':
                pass  # TODO: self.frame_index = 0
            self.status = 'attack'
        else:
            self.status = 'move'

    def actions(self, player):
        # faz uma ação baseado no status atual
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.can_attack = False  # TODO: passar para a lógica do animate() ao adicionar sprites
            player.damage(self.collision_damage)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def damage(self, damage, player):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            self.kill()

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction = pygame.math.Vector2()  # fazer o inimigo parar ao tomar um ataque

    def move(self, speed, collision_hitbox_name='hitbox'):
        # o move() está sendo reescrito somente para atualizar a posição do damage_hitbox
        super().move(speed, collision_hitbox_name)
        self.damage_hitbox.center = self.hitbox.center

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self, player):
        # esse enemy_update() é diferente do update() por receber o parâmetro player
        # ele também é chamado dentro do Level, mas, por ter uma assinatura diferente do update()
        # dos outros sprites, não pode ser chamado da mesma forma que eles
        self.get_status(player)
        self.actions(player)
