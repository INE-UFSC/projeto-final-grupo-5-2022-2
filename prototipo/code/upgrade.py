from abc import abstractmethod, ABC

from utils import load_sprite


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


class FireRateUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Fire Rate Upgrade',
                         'Esta descrição é um teste para conferir se a UI está separando as linhas corretamente',
                         '/test/icon_fire_rate_upgrade.png')

    def apply(self, player):
        player.attacks[0].cooldown *= 0.9
