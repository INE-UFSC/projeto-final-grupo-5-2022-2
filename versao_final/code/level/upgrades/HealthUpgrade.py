from code.level.upgrades.Upgrade import Upgrade
from code.level.GroupManager import GroupManager


class HealthUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Health Upgrade',
                         'Aumenta a quantidade de vidas em 1',
                         '/icons/health_upgrade.png')

    def apply(self):
        GroupManager().player.give_health(1)
