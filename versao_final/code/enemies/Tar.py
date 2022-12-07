from code.enemies.BasicEnemy import Enemy


class Tar(Enemy):
    def __init__(self, pos):
        super().__init__('tar', pos, health=3, speed=1.5, collision_damage=1, exp=1, attack_cooldown=85)
