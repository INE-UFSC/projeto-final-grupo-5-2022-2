from code.level.enemies.BasicEnemy import Enemy


class Zombie(Enemy):
    def __init__(self, pos):
        super().__init__('zombie', pos, health=4, speed=2, collision_damage=2, exp=5, attack_cooldown=60)
