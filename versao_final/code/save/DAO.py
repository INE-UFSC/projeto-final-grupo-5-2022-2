import pickle
from abc import ABC, abstractmethod
from code.library.Settings import Settings

class DAO(ABC):
    def __init__(self, datasource):
        self.__settings = Settings()
        self.__datasource = f'{self.__settings.SAVE_PATH}/{datasource}'
        self.__object_cache = None
        try:
            self.__load()
        except FileNotFoundError:
            self.__dump()

    def __dump(self):
        pickle.dump(self.__cache, open(self.__datasource, "wb"))

    def __load(self):
        self.__object_cache = pickle.load(open(self.__datasource, "rb"))

    @abstractmethod
    def add(self, key, obj):
        self.__object_cache[key] = obj
        self.__dump()

    @abstractmethod
    def get(self, key):
        try:
            return self.__object_cache[key]
        except KeyError:
            return None
    
    @abstractmethod
    def remove(self, key):
        try:
            self.__object_cache.pop(key)
            self.__dump()
        except KeyError:
            pass
    
    @abstractmethod
    def get_all(self):
        return self.__object_cache.values()