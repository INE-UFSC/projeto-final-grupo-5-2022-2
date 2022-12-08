from code.level.upgrades.Upgrade import Upgrade
from code.level.GroupManager import GroupManager


class SpeedUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Speed Upgrade',
                         'Aumenta a velocidade em 5%',
                         '/icons/speed_upgrade.png')

    def apply(self):
        player = GroupManager().player
        player.move_speed = player.move_speed + player.base_speed * 0.05
