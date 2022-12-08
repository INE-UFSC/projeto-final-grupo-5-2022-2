from abc import ABC, abstractmethod


class IScene(ABC):
    @abstractmethod
    def run(self):
        pass
