import pygame.math

from code.particles import *
from code.player import Player
from code.settings import *
from code.group_manager import GroupManager
from code.room import Room


class Level:
    def __init__(self):
        self.__group_manager = GroupManager()   
        # player
        self.player = Player([self.__group_manager.visible_sprites], [self.__group_manager.visible_sprites, self.__group_manager.attack_sprites],
                                         self.__group_manager.obstacle_sprites)
        # salas
        self.__room_list = list([Room(ROOM_MAP_1, self.player), Room(ROOM_MAP_2, self.player)])
        self.__current_room_index = 0
        self.current_room.create_map()

    @property
    def current_room(self):
        return self.__room_list[self.__current_room_index]
        
    def next_room(self):
        if self.__current_room_index < len(self.__room_list) - 1:
            self.__current_room_index += 1
            self.__group_manager.clear_all_groups()
            self.current_room.create_map()
        else:
            self.end_level()
            
    def end_level(self):
        print("Level end")

    def toggle_menu(self):
        self.current_room.toggle_menu()

    def run(self):
        self.current_room.run()
        if self.current_room.player.rect.topleft[0] > WIDTH - 192: # mudar
            self.next_room()
        

