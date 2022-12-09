from code.save.DAO import DAO
from code.scenes.LevelScene import LevelScene


class LevelSceneDAO(DAO):
    def __init__(self, save_name):
        super().__init__(f'{save_name}.pkl')

    def add(self, level_scene):
        if level_scene is not None and isinstance(level_scene, LevelScene):
            super().add('level_scene', level_scene)

    def get(self) -> LevelScene:
        return super().get('level_scene')

    def remove(self):
        super().remove('level_scene')

    def get_all(self):
        return super().get_all()