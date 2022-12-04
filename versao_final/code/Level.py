from code.Fade import Fade
from code.GroupManager import GroupManager
from code.Room import Room
from code.Settings import *


class Level:
    def __init__(self, rooms: tuple):
        # salas
        self.__rooms = rooms
        self.__current_room_index = 0
        self.__room = Room(self.__rooms[self.__current_room_index])
        self.__changing_room = False

        self.__fade = Fade(in_step=8, out_step=-2, alpha=0)
        GroupManager().add_to_persistent(self.__fade)

    def next_room(self):
        if self.__current_room_index < len(self.__rooms) - 1:
            self.__current_room_index += 1
            self.__room.change_to(self.__rooms[self.__current_room_index])
            self.__fade.fade_out()
        else:
            self.end_level()

    def end_level(self):
        print("Level end")

    def toggle_menu(self):
        self.__room.toggle_menu()

    def run(self):
        self.__room.run()

        self.__fade.animate()
        if self.__changing_room and self.__fade.animation_ended():
            self.__changing_room = False
            self.next_room()

        if self.__room.room_ended():
            # TODO: melhorar a condição de troca de sala
            # a parte de conferir a posição do player acho melhor passar para o room_ended() da sala
            if GroupManager().player.rect.topleft[0] > WIDTH - 192 and not self.__changing_room:  # mudar
                self.__changing_room = True
                self.__fade.fade_in()
