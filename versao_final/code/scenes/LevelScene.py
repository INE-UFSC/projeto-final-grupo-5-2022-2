from code.level.Fade import Fade
from code.level.GroupManager import GroupManager
from code.level.Room import Room
from code.level.particles.AnimationParticle import AnimationParticle
from code.library.Resources import Resources
from code.library.Settings import Settings
from code.scenes.ILevelScene import ILevelScene


class LevelScene(ILevelScene):
    def __init__(self, change_to_scene):
        super().__init__(change_to_scene)
        group_manager = GroupManager()
        group_manager.nuke()  # limpar os sprites persistentes também
        self.__settings = Settings()
        self.__rooms = ('1', '2')
        self.__current_room_index = 0
        self.__room = Room(self.__rooms[self.__current_room_index])
        self.__changing_room = False

        self.__fade = Fade(in_step=16, out_step=-8, alpha=0)
        group_manager.add_to_persistent(self.__fade)
        # a seta está sendo definida no LevelScene em vez de no Room para ter acesso
        # ao atributo changing_room
        arrow_animation = Resources().get_animation('/icons/arrow')
        arrow_x = 1280 - 96
        arrow_y = self.__settings.HEIGHT // 2
        self.__arrow = AnimationParticle((arrow_x, arrow_y), arrow_animation, 0.1)
        self.__arrow.sprite_type = 'effect'
        self.__arrow.image.set_alpha(0)
        group_manager.add_to_persistent(self.__arrow)

    def run(self):
        self.__room.run()

        # efeitos (fade e seta)
        self.__fade.animate()
        if self.__changing_room and self.__fade.animation_ended():
            self.__changing_room = False
            self.go_to_next_room()

        arrow_alpha = 255 if self.__room.room_ended and not self.__changing_room else 0
        self.__arrow.image.set_alpha(arrow_alpha)

        # lógica de próxima sala
        if self.__room.room_ended:
            # TODO: melhorar a condição de troca de sala
            # a parte de conferir a posição do player acho melhor passar para o room_ended da sala
            if GroupManager().player.rect.topleft[
                0] > self.__settings.WIDTH - self.__settings.LEVEL_CHANGE_DISTANCE and not self.__changing_room:  # mudar
                self.__changing_room = True
                self.__fade.fade_in()

        # morte do player
        if self.__room.is_player_dead:
            self.change_to_scene('death')

    def go_to_next_room(self):
        if self.__current_room_index < len(self.__rooms) - 1:
            self.__current_room_index += 1
            self.__room.change_to(self.__rooms[self.__current_room_index])
            self.__fade.fade_out()
        else:
            self.end()

    def end(self):
        self.change_to_scene('win')

    def toggle_menu(self):
        self.__room.toggle_menu()
