from code.enemies.BasicEnemy import Enemy


class Bat(Enemy):
    def __init__(self, pos):
        super().__init__('bat', pos, health=1, speed=3, collision_damage=1, exp=1,
                         attack_cooldown=40)
