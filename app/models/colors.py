from pydantic.color import Color
from enum import Enum

class ColorExamples_en(Color,Enum):
    BLACK = 'black'
    WHITE = 'white'
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'
    YELLOW = 'yellow'
    CYAN = 'cyan'
    MAGENTA = 'magenta'
    ORANGE = 'orange'
    PURPLE = 'purple'
    PINK = 'pink'
    LIME = 'lime'
    TEAL = 'teal'
    AQUA = 'aqua'
    NAVY = 'navy'
    MAROON = 'maroon'
    OLIVE = 'olive'
    SILVER = 'silver'
    GRAY = 'gray'


class ColorCombination(Enum):
    RED_GREEN = ('#FF0000', '#00FF00')
    BLUE_YELLOW = ('#0000FF', '#FFFF00')
    PURPLE_ORANGE = ('#800080', '#FFA500')
    TEAL_PINK = ('#008080', '#FFC0CB')
    NAVY_GOLD = ('#000080', '#FFD700')
    GREEN_PURPLE = ('#008000', '#800080')
    ORANGE_BLUE = ('#FFA500', '#0000FF')
    PINK_GREEN = ('#FFC0CB', '#008000')
    YELLOW_RED = ('#FFFF00', '#FF0000')
    SILVER_BLUE = ('#C0C0C0', '#0000FF')

