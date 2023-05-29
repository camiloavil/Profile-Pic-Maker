from enum import Enum

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CUSTOM_COLOR_1 = (100, 150, 200)
    CUSTOM_COLOR_2 = (50, 100, 150)

class FlatUIColors(Color):
    TURQUOISE = (26, 188, 156)
    EMERALD = (46, 204, 113)
    PETER_RIVER = (52, 152, 219)
    AMETHYST = (155, 89, 182)
    WET_ASPHALT = (52, 73, 94)
    GREEN_SEA = (22, 160, 133)
    NEPHRITIS = (39, 174, 96)
    BELIZE_HOLE = (41, 128, 185)
    WISTERIA = (142, 68, 173)
    MIDNIGHT_BLUE = (44, 62, 80)

class MaterialDesignColors(Color):
    RED_500 = (244, 67, 54)
    PINK_500 = (233, 30, 99)
    PURPLE_500 = (156, 39, 176)
    DEEP_PURPLE_500 = (103, 58, 183)
    INDIGO_500 = (63, 81, 181)
    BLUE_500 = (33, 150, 243)
    LIGHT_BLUE_500 = (3, 169, 244)
    CYAN_500 = (0, 188, 212)
    TEAL_500 = (0, 150, 136)
    GREEN_500 = (76, 175, 80)

class MaterialDesignAccentColors(Color):
    RED_A200 = (239, 83, 80)
    PINK_A200 = (233, 30, 99)
    PURPLE_A200 = (186, 104, 200)
    DEEP_PURPLE_A200 = (159, 89, 214)
    INDIGO_A200 = (92, 107, 192)
    BLUE_A200 = (68, 138, 255)
    LIGHT_BLUE_A200 = (41, 121, 255)
    CYAN_A200 = (0, 229, 255)
    TEAL_A200 = (0, 191, 165)
    GREEN_A200 = (100, 221, 23)

class BootstrapColors(Color):
    PRIMARY = (0, 123, 255)
    SECONDARY = (108, 117, 125)
    SUCCESS = (40, 167, 69)
    DANGER = (220, 53, 69)
    WARNING = (255, 193, 7)
    INFO = (23, 162, 184)
    LIGHT = (248, 249, 250)
    DARK = (52, 58, 64)
