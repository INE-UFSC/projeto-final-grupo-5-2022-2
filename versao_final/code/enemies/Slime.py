from code.enemies.BasicEnemy import Enemy


class Slime(Enemy):
    def __init__(self, pos):
        super().__init__('slime', pos, health=2, speed=3, collision_damage=1, exp=3, attack_cooldown=50)
