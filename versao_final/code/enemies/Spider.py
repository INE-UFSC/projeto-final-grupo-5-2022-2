from code.enemies.Ranged import Ranged


class Spider(Ranged):
    def __init__(self, pos):
        super().__init__('spider', pos, range=1000, target_distance=500, 
                         projectile_sprite='/enemies/attacks/web.png', projectile_damage=1,
                         projectile_speed=5, health=2, speed=4, collision_damage=1, exp=3,
                         attack_cooldown=40)