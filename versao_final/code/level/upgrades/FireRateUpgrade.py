from code.level.upgrades.Upgrade import Upgrade
from code.level.GroupManager import GroupManager


class FireRateUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Fire Rate Upgrade',
                         'Reduz 5% do cooldown da bola de fogo',
                         '/icons/fire_rate_upgrade.png')

    def apply(self):
        GroupManager().player.attacks[0].cooldown *= 0.95
