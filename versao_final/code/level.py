from code.Fade import Fade
from code.GroupManager import GroupManager
from code.Room import Room
from code.Settings import *


class Level:
    def __init__(self):
        # salas
        self.__rooms = ('1', '2')
        self.__current_room_index = 0
        self.__room = Room(self.__rooms[self.__current_room_index])
        self.__changing_room = False

    def next_room(self):
        if self.__current_room_index < len(self.__rooms) - 1:
            self.__current_room_index += 1
            self.__room.change_to(self.__rooms[self.__current_room_index])
            # TODO: arrumar o fade out
            self.__Fade = Fade(fade_step=3, fade_in=True)
        else:
            self.end_level()

    def end_level(self):
        print("Level end")

    def toggle_menu(self):
        self.__room.toggle_menu()

    def run(self):
        self.__room.run()

        if hasattr(self, '_Level__Fade') and self.__Fade.step():
            if self.__changing_room:
                self.__changing_room = False
                self.next_room()
            self.__Fade.kill()

        if self.__room.room_ended():
            # TODO: melhorar a condição de troca de sala
            # a parte de conferir a posição do player acho melhor passar para o room_ended() da sala
            if GroupManager().player.rect.topleft[0] > WIDTH - 192 and not self.__changing_room:  # mudar
                self.__Fade = Fade(fade_step=3, fade_in=False)
                self.__changing_room = True
