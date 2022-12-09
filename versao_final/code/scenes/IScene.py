from abc import ABC, abstractmethod


class IScene(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def change_to_scene(self):
        pass
