import random

from code.enemies.Bat import Bat
from code.enemies.Spider import Spider
from code.Resources import Resources
from code.Settings import *


class WaveManager:
    def __init__(self):
        self.__enemy_classes = {'bat': Bat, 'spider' : Spider}  # TODO: passar para o singleton dos settings
        self.__wave_data = None
        self.__timer = 0
        self.__tick_index = 0
        self.__max_time = WAVE_TIME
        self.__spawn_positions = ((200, 200), (500, 500))

    def change_to_wave(self, room_name):
        self.__wave_data = Resources().get_wave(room_name)
        self.__timer = 0
        self.__tick_index = 0

    def wave_ended(self):
        return self.__timer >= self.__max_time

    def update(self):
        if self.__wave_data is None or self.wave_ended():
            return

        self.__timer += 1

        # lógica de avançar tick
        while len(self.__wave_data['ticks']) - 1 > self.__tick_index and \
                self.__timer >= self.__wave_data['ticks'][self.__tick_index + 1]['timer']:
            self.__tick_index += 1

        tick = self.__wave_data['ticks'][self.__tick_index]['every']
        # spawn de inimigos
        if self.__timer % tick == 0:
            available_spawns = [spawn for spawn in self.__wave_data['spawns'] if
                                spawn['after'] <= self.__timer <= spawn['before']]
            chosen_spawn = random.choice(available_spawns)
            enemies = chosen_spawn['enemies'].split('/')
            locations = chosen_spawn['locations'].split('/')
            for enemy_name, location in zip(enemies, locations):
                # as localizações possíveis atualmente são:
                # random - escolhe uma posiçaõ aleatoriamente
                # previous - spawna na mesma posição do anterior
                if location == 'random':
                    spawn_position = random.choice(self.__spawn_positions)
                self.__enemy_classes[enemy_name](spawn_position)

    @property
    def timer(self):
        return self.__timer

    @property
    def tick_index(self):
        return self.__tick_index

    @property
    def max_time(self):
        return self.__max_time

    @property
    def spawn_positions(self):
        return self.__spawn_positions
