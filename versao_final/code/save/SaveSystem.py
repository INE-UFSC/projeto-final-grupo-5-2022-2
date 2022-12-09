from code.library.Settings import Settings
from code.save.PlayerDAO import PlayerDAO
from code.save.LevelSceneDAO import LevelSceneDAO


class SaveSystem():
    def __init__(self, player):
        self.__settings = Settings()
        self.save_file = ''

    def save_game(self):
        