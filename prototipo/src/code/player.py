import pygame

from entity import Entity


class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.speed = 5

        self.obstacle_sprites = obstacle_sprites

        # ataque básico
        self.attack_cooldown = 180
        self.can_attack = True
        self.attack_time = 0
        self.create_attack = create_attack

    def input(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # movimento vertical
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # movimento horizontal
        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # ataque
        if mouse[0] and self.can_attack:
            self.create_attack()
            self.can_attack = False
            self.attack_time = pygame.time.get_ticks()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if not self.can_attack and current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True

    def update(self):
        self.input()
        self.move(self.speed)
        self.cooldowns()
