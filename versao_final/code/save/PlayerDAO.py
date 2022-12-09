from code.save.DAO import DAO
from code.level.Player import Player


class PlayerDAO(DAO):
    def __init__(self, save_name):
        super().__init__(f'{save_name}.pkl')

    def add(self, player):
        if player is not None and isinstance(player, Player):
            super().add('player', player)

    def get(self) -> Player:
        return super().get('player')

    def remove(self):
        super().remove('player')

    def get_all(self):
        return super().get_all()