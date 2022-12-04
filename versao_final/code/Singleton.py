class Singleton(object):
    __instance = None

    # sobrescrita do magic method __new__ para
    # ser nosso getInstance
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            cls.__instance._initialized = False
        return cls.__instance
