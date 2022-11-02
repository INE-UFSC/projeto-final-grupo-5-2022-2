from abc import abstractmethod, ABC

from player import Player
from utils import load_sprite


class Upgrade(ABC):
    def __init__(self, name, description, icon):
        self.name = name
        self.description = description
        self.icon = load_sprite(icon)

    @abstractmethod
    def apply(self, player):
        pass


class FireRateUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Fire Rate Upgrade', 'DESCRICAO', '/test/icon_fire_rate_upgrade.png')

    def apply(self, player: Player):
        player.attacks[0].cooldown *= 0.9
