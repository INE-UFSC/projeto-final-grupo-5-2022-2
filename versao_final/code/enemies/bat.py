from code.enemies.enemy import Enemy


class Bat(Enemy):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__('bat', pos, groups, obstacle_sprites, health=1, speed=3, collision_damage=1, exp=1,
                         attack_cooldown=40)
