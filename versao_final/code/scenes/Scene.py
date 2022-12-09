from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, change_to_scene):
        self.__change_to_scene = change_to_scene

    @abstractmethod
    def run(self):
        pass

    @property
    def change_to_scene(self):
        return self.__change_to_scene
