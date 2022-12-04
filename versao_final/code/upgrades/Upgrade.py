from abc import ABC, abstractmethod
from code.Resources import Resources


class Upgrade(ABC):
    def __init__(self, name, description, icon):
        self.__name = name
        self.__description = description
        self.__icon = Resources().get_sprite(icon)

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
        return self.__icon


