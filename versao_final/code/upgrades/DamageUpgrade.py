from code.upgrades.Upgrade import Upgrade
from code.GroupManager import GroupManager


class DamageUpgrade(Upgrade):
    def __init__(self):
        super().__init__('Damage Upgrade',
                         'Aumenta o dano da bola de fogo em 20%',
                         '/icons/damage_upgrade.png')

    def apply(self):
        player = GroupManager().player
        player.attacks[0].damage += player.attacks[0].base_damage * 0.20
