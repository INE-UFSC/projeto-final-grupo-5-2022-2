from code.group_manager import GroupManager
from code.room import Room
from code.settings import WIDTH


class Level:
    def __init__(self):
        self.__group_manager = GroupManager()
        # player
        # self.player = Player([self.__group_manager.visible_sprites],
        #                     [self.__group_manager.visible_sprites, self.__group_manager.attack_sprites],
        #                     self.__group_manager.obstacle_sprites)
        # salas
        self.__rooms = ('1', '2')
        self.__current_room_index = 0
        self.__room = Room(self.__rooms[self.__current_room_index])

    def toggle_menu(self):
        self.__room.toggle_menu()

    def run(self):
        self.__room.run()
        if self.__room.player.rect.topleft[0] > WIDTH - 192 and \
                self.__current_room_index < len(self.__rooms) - 1:  # mudar
            self.__current_room_index += 1
            self.__room.change_to(self.__rooms[self.__current_room_index])
