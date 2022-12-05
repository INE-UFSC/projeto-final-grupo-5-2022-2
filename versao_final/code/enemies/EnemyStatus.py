from enum import Enum


class RangedStatus(Enum):
    MOVE = 0
    ATTACK = 1
    FLEE = 2
    MELEE = 3

class Melee_Status(Enum):
    MOVE = 0
    ATTACK = 1