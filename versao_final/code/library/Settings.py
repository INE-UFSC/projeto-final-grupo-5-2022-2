import os

from code.library.Singleton import Singleton


class Settings(Singleton):
    def __init__(self) -> None:
        super().__init__()
        if not self._initialized:
            self._initialized = True

            self.__WIDTH = 1280
            self.__HEIGHT = 720
            self.__FPS = 60
            self.__TILESIZE = 64

            # Para o executável funcionar corretamente precisa adicionar mais um os.pardir
            # no os.path.join abaixo.
            self.__GAME_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir, os.pardir))
            
            self.__SAVE_PATH = f'{self.__GAME_PATH}/saves'
            self.__save_name = 'save'
            self.__new_game = False

            self.__COLOR_BLACK = (0, 0, 0)
            self.__WHITE = '#ffffff'

            self.__UI_FONT = f'{self.__GAME_PATH}/graphics/font/joystix.ttf'
            self.__UI_FONT_SIZE = 18
            self.__UI_BG_COLOR = '#262b44'
            self.__UI_BORDER_COLOR = '#181425'
            self.__UI_BORDER_COLOR_ACTIVE = '#FFFFFF'
            self.__UI_HOVER_COLOR = '#3a4466'
            self.__TEXT_COLOR = '#EEEEEE'
            self.__ITEM_BOX_SIZE = 64
            self.__BAR_HEIGHT = 32
            self.__EXP_BAR_WIDTH = 176
            self.__EXP_BAR_COLOR = '#0099db'
            self.__STAT_BAR_WIDTH = 384
            self.__UI_COMPONENT_MARGIN = 10

            self.__UPGRADE_BUTTON_RIGHT_MARGIN = 704
            self.__UPGRADE_BUTTON_TOP = 128
            self.__UPGRADE_BUTTON_SPACING = 192
            self.__UPGRADE_TITLE_TOP = 64
            self.__UPGRADE_BUTTON_WIDTH = 576
            self.__UPGRADE_BUTTON_HEIGHT = 128
            self.__STAT_LEFT_MARGIN = 128
            self.__STAT_TOP_MARGIN = 256
            self.__STAT_SPACING = 64
            self.__MENU_LOGO_TOP = 96
            self.__TEXT_BUTTON_WIDTH = 576
            self.__TEXT_BUTTON_HEIGHT = 64
            self.__EXIT_BUTTON_WIDTH = 400

            self.__X_OFFSET = {'': 0, '0': -16}
            self.__Y_OFFSET = {'': 0, '0': -40}
            self.__SMALL_HITBOX_OFFSET = {'': -50}

            self.__WAVE_TIME = 5400  # 1 minuto e 30 segundos

            self.__LEVEL_CHANGE_DISTANCE = 64

    # Getters de todas as variáveis
    @property
    def WIDTH(self) -> int:
        return self.__WIDTH

    @property
    def HEIGHT(self) -> int:
        return self.__HEIGHT

    @property
    def FPS(self) -> int:
        return self.__FPS

    @property
    def TILESIZE(self) -> int:
        return self.__TILESIZE

    @property
    def GAME_PATH(self) -> str:
        return self.__GAME_PATH

    @property
    def SAVE_PATH(self) -> str:
        return self.__SAVE_PATH

    @property
    def save_name(self) -> str:
        return self.__save_name

    @save_name.setter
    def save_name(self, value: str) -> None:
        self.__save_name = value

    @property
    def new_game(self) -> bool:
        return self.__new_game

    @new_game.setter
    def new_game(self, value: bool) -> None:
        self.__new_game = value

    @property
    def COLOR_BLACK(self) -> tuple:
        return self.__COLOR_BLACK

    @property
    def WHITE(self) -> str:
        return self.__WHITE

    @property
    def UI_FONT(self) -> str:
        return self.__UI_FONT

    @property
    def UI_FONT_SIZE(self) -> int:
        return self.__UI_FONT_SIZE

    @property
    def UI_BG_COLOR(self) -> str:
        return self.__UI_BG_COLOR

    @property
    def UI_BORDER_COLOR(self) -> str:
        return self.__UI_BORDER_COLOR

    @property
    def UI_BORDER_COLOR_ACTIVE(self) -> str:
        return self.__UI_BORDER_COLOR_ACTIVE

    @property
    def UI_HOVER_COLOR(self) -> str:
        return self.__UI_HOVER_COLOR

    @property
    def TEXT_COLOR(self) -> str:
        return self.__TEXT_COLOR

    @property
    def ITEM_BOX_SIZE(self) -> int:
        return self.__ITEM_BOX_SIZE

    @property
    def BAR_HEIGHT(self) -> int:
        return self.__BAR_HEIGHT

    @property
    def EXP_BAR_WIDTH(self) -> int:
        return self.__EXP_BAR_WIDTH

    @property
    def EXP_BAR_COLOR(self) -> str:
        return self.__EXP_BAR_COLOR

    @property
    def STAT_BAR_WIDTH(self) -> int:
        return self.__STAT_BAR_WIDTH

    @property
    def UI_COMPONENT_MARGIN(self) -> int:
        return self.__UI_COMPONENT_MARGIN

    @property
    def UPGRADE_BUTTON_RIGHT_MARGIN(self) -> int:
        return self.__UPGRADE_BUTTON_RIGHT_MARGIN

    @property
    def UPGRADE_BUTTON_TOP(self) -> int:
        return self.__UPGRADE_BUTTON_TOP

    @property
    def UPGRADE_BUTTON_SPACING(self) -> int:
        return self.__UPGRADE_BUTTON_SPACING

    @property
    def UPGRADE_TITLE_TOP(self) -> int:
        return self.__UPGRADE_TITLE_TOP

    @property
    def UPGRADE_BUTTON_WIDTH(self) -> int:
        return self.__UPGRADE_BUTTON_WIDTH

    @property
    def UPGRADE_BUTTON_HEIGHT(self) -> int:
        return self.__UPGRADE_BUTTON_HEIGHT

    @property
    def STAT_LEFT_MARGIN(self) -> int:
        return self.__STAT_LEFT_MARGIN

    @property
    def STAT_TOP_MARGIN(self) -> int:
        return self.__STAT_TOP_MARGIN

    @property
    def STAT_SPACING(self) -> int:
        return self.__STAT_SPACING

    @property
    def MENU_LOGO_TOP(self) -> int:
        return self.__MENU_LOGO_TOP

    @property
    def TEXT_BUTTON_WIDTH(self) -> int:
        return self.__TEXT_BUTTON_WIDTH

    @property
    def TEXT_BUTTON_HEIGHT(self) -> int:
        return self.__TEXT_BUTTON_HEIGHT

    @property
    def EXIT_BUTTON_WIDTH(self) -> int:
        return self.__EXIT_BUTTON_WIDTH

    @property
    def X_OFFSET(self) -> dict:
        return self.__X_OFFSET

    @property
    def Y_OFFSET(self) -> dict:
        return self.__Y_OFFSET

    @property
    def SMALL_HITBOX_OFFSET(self) -> dict:
        return self.__SMALL_HITBOX_OFFSET

    @property
    def WAVE_TIME(self) -> int:
        return self.__WAVE_TIME

    @property
    def LEVEL_CHANGE_DISTANCE(self) -> int:
        return self.__LEVEL_CHANGE_DISTANCE
