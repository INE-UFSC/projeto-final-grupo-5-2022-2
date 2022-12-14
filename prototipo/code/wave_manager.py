import random

from code.resources import Resources
from code.settings import *


class WaveManager:
    def __init__(self):
        self.__wave_data = None
        self.__timer = 0
        self.__tick_index = 0
        self.__max_time = WAVE_TIME
        self.__spawn_positions = ((200, 200), (500, 500))

    def change_to_wave(self, room_name):
        self.__wave_data = Resources().get_wave(room_name)
        self.__timer = 0
        self.__tick_index = 0

    def update(self, spawn_enemy):
        if self.__wave_data is None:
            return

        if self.__timer >= self.__max_time:
            return

        self.__timer += 1

        # lógica de avançar tick
        while len(self.__wave_data['ticks']) - 1 > self.__tick_index and \
                self.__timer >= self.__wave_data['ticks'][self.__tick_index + 1]['timer']:
            self.__tick_index += 1

        tick = self.__wave_data['ticks'][self.__tick_index]['every']
        # spawn de inimigos
        if self.__timer % tick == 0:
            available_spawns = list(
                filter(lambda spawn: spawn['after'] <= self.__timer <= spawn['before'],
                       self.__wave_data['spawns']))
            chosen_spawn = random.choice(available_spawns)
            enemies = chosen_spawn['enemies'].split('/')
            locations = chosen_spawn['locations'].split('/')
            for enemy, location in zip(enemies, locations):
                # as localizações possíveis atualmente são:
                # random - escolhe uma posiçaõ aleatoriamente
                # previous - spawna na mesma posição do anterior
                if location == 'random':
                    spawn_position = random.choice(self.__spawn_positions)
                spawn_enemy(enemy, spawn_position)

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
