from code.enemies.Ranged import Ranged


class Spider(Ranged):
    def __init__(self, pos):
        super().__init__('spider', pos, range=200, target_distance=150, flee_distance=100,
                         projectile_damage=1,
                         projectile_speed=7, health=2, speed=4, collision_damage=0, exp=3,
                         attack_cooldown=40)