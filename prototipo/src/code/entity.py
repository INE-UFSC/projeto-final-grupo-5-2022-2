import pygame.sprite


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.direction = pygame.math.Vector2()

    def move(self, speed):
        if self.direction.magnitude() != 0:
            # manter a velocidade caso o player esteja indo em na diagonal
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        collided = False or self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        collided = collided or self.collision('vertical')
        # manter a hitbox nos pés da entidade
        self.rect.centerx = self.hitbox.centerx
        self.rect.bottom = self.hitbox.bottom
        return not collided

    def collision(self, direction):
        collided = False
        # colisão horizontal
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    collided = True
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        # colisão vertical
        elif direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    collided = True
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
        return collided
