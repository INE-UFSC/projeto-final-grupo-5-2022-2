from code.level.Fade import Fade
from code.level.GroupManager import GroupManager
from code.level.Room import Room
from code.library.Settings import Settings
from code.scenes.ILevelScene import ILevelScene


class LevelScene(ILevelScene):
    def __init__(self):
        self.__settings = Settings()
        self.__rooms = ('1', '2')
        self.__current_room_index = 0
        self.__room = Room(self.__rooms[self.__current_room_index])
        self.__changing_room = False

        self.__fade = Fade(in_step=8, out_step=-2, alpha=0)
        GroupManager().add_to_persistent(self.__fade)

    def run(self):
        self.__room.run()

        self.__fade.animate()
        if self.__changing_room and self.__fade.animation_ended():
            self.__changing_room = False
            self.go_to_next_room()

        if self.__room.room_ended():
            # TODO: melhorar a condição de troca de sala
            # a parte de conferir a posição do player acho melhor passar para o room_ended() da sala
            if GroupManager().player.rect.topleft[0] > self.__settings.WIDTH - 192 and not self.__changing_room:  # mudar
                self.__changing_room = True
                self.__fade.fade_in()

    def go_to_next_room(self):
        if self.__current_room_index < len(self.__rooms) - 1:
            self.__current_room_index += 1
            self.__room.change_to(self.__rooms[self.__current_room_index])
            self.__fade.fade_out()
        else:
            self.end_level()

    def end(self):
        print("Level end")  # TODO: Menu de morte

    def toggle_menu(self):
        self.__room.toggle_menu()
