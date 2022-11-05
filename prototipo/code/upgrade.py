from abc import abstractmethod, ABC

from code.utils import load_sprite


class Upgrade(ABC):
    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = load_sprite(icon)

    @abstractmethod
    def apply(self, player):
        pass


class HealthUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Health Upgrade',
                         'Aumenta a quantidade de vidas em 1',
                         '/icon/health_upgrade.png')

    def apply(self, player):
        player.give_health(1)


class DamageUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Damage Upgrade',
                         'Aumenta o dano da bola de fogo em 20%',
                         '/icon/damage_upgrade.png')

    def apply(self, player):
        player.attacks[0].damage += player.attacks[0].base_damage * 0.20


class FireRateUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Fire Rate Upgrade',
                         'Reduz 5% do cooldown da bola de fogo',
                         '/icon/fire_rate_upgrade.png')

    def apply(self, player):
        player.attacks[0].cooldown *= 0.95


class SpeedUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Speed Upgrade',
                         'Aumenta a velocidade em 5%',
                         '/icon/speed_upgrade.png')

    def apply(self, player):
        player.move_speed = player.move_speed + player.base_speed * 0.05