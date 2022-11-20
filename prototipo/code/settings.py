import os

WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64

# Para o executável funcionar corretamente precisa adicionar mais um os.pardir
# no os.path.join abaixo.
GAME_PATH = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

COLOR_BLACK = (0, 0, 0)
WHITE = '#ffffff'

UI_FONT = f'{GAME_PATH}/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
UI_BORDER_COLOR_ACTIVE = '#FFFFFF'
UI_HOVER_COLOR = '#424242'
TEXT_COLOR = '#EEEEEE'
ITEM_BOX_SIZE = 64
BAR_HEIGHT = 32
EXP_BAR_WIDTH = 176
EXP_BAR_COLOR = '#0099db'
STAT_BAR_WIDTH = 384

WORLD_MAP = [
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', 'p', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x'],
    ['x', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'x', ' ', 'x'],
    ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
]

WAVE_TIME = 5400  # 1 minuto e 30 segundos