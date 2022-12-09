from abc import ABC, abstractmethod

from code.scenes.IScene import IScene
from code.scenes.Scene import Scene


class ILevelScene(Scene, IScene, ABC):
    def __init__(self, change_to_scene):
        super().__init__(change_to_scene)

    @abstractmethod
    def go_to_next_room(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def toggle_menu(self):
        pass
