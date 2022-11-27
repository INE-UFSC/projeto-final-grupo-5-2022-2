class Singleton(object):
    __instance = None

    # sobrescrita do magic method __new__ para
    # ser nosso getInstance
    def __new__(cls, *args):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls, *args)
        return cls.__instance
