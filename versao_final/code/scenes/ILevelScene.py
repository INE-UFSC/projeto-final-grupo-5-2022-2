from abc import ABC, abstractmethod

from code.scenes.IScene import IScene


class ILevelScene(IScene, ABC):
    @abstractmethod
    def go_to_next_room(self):
        pass

    @abstractmethod
    def end(self):
        pass

    @abstractmethod
    def toggle_menu(self):
        pass
