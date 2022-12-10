from abc import ABC, abstractmethod
from code.library.Resources import Resources


class Upgrade(ABC):
    def __init__(self, name, description, icon):
        self.__name = name
        self.__description = description
        self.__icon = icon

    @abstractmethod
    def apply(self):
        pass

    @property
    def name(self):
        return self.__name

    @property
    def description(self):
        return self.__description

    @property
    def icon(self):
        return Resources().get_sprite(self.__icon)


