from code.save.DAO import DAO


class PlayerDAO(DAO):
    def __init__(self):
        super().__init__('player.pkl')

    def add(self, key, obj):
        if obj is not None:
            super().add(f'{key}', obj)

    def get(self, key):
        return super().get(f'{key}')

    def remove(self, key):
        super().remove(f'{key}')

    def get_all(self):
        return super().get_all()