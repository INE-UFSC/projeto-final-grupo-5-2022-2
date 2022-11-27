from code.room import Room
from code.settings import WIDTH


class Level:
    def __init__(self):
        # salas
        self.__rooms = ('1', '2')
        self.__current_room_index = 0
        self.__room = Room(self.__rooms[self.__current_room_index])

    def next_room(self):
        if self.__current_room_index < len(self.__rooms) - 1:
            self.__current_room_index += 1
            self.__room.change_to(self.__rooms[self.__current_room_index])
        else:
            self.end_level()

    def end_level(self):
        print("Level end")

    def toggle_menu(self):
        self.__room.toggle_menu()

    def run(self):
        self.__room.run()
        # TODO: conferir se a wave já terminou
        if self.__room.player.rect.topleft[0] > WIDTH - 192:  # mudar
            self.next_room()
