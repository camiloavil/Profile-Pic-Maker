from enum import Enum

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    BLUE_SKY = (135, 206, 250)   # Azul claro
    CUSTOM_COLOR_1 = (100, 150, 200)
    CUSTOM_COLOR_2 = (50, 100, 150)
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
    INDIGO_500 = (63, 81, 181)
    RED_500 = (244, 67, 54)
    PINK_500 = (233, 30, 99)
    PURPLE_500 = (156, 39, 176)
    DEEP_PURPLE_500 = (103, 58, 183)
    BLUE_500 = (33, 150, 243)
    LIGHT_BLUE_500 = (3, 169, 244)
    CYAN_500 = (0, 188, 212)
    TEAL_500 = (0, 150, 136)
    GREEN_500 = (76, 175, 80)
    PRIMARY = (0, 123, 255)
    SECONDARY = (108, 117, 125)
    SUCCESS = (40, 167, 69)
    DANGER = (220, 53, 69)
    WARNING = (255, 193, 7)
    INFO = (23, 162, 184)
    LIGHT = (248, 249, 250)
    DARK = (52, 58, 64)
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

class Colors(Enum):
    BLUE_SKY_TO_INDIGO = (Color.BLUE_SKY, Color.INDIGO_500)
    RED_TO_BLACK = (Color.RED_500, Color.BLACK)
    LIGHT_BLUE_A200_TO_BLACK = (Color.LIGHT_BLUE_A200, Color.BLACK)
    CUSTOM_COLORS_1_TO_2 = (Color.CUSTOM_COLOR_1, Color.CUSTOM_COLOR_2)
    TURQUOISE_TO_EMERALD = (Color.TURQUOISE, Color.EMERALD)
    PETER_RIVER_TO_AMETHYST = (Color.PETER_RIVER, Color.AMETHYST)
    WET_ASPHALT_TO_GREEN_SEA = (Color.WET_ASPHALT, Color.GREEN_SEA)
    NEPHRITIS_TO_BELIZE_HOLE = (Color.NEPHRITIS, Color.BELIZE_HOLE)
    WISTERIA_TO_MIDNIGHT_BLUE = (Color.WISTERIA, Color.MIDNIGHT_BLUE)
    RED_500_TO_PURPLE_500 = (Color.RED_500, Color.PURPLE_500)
    BLUE_A200_TO_TEAL_A200 = (Color.BLUE_A200, Color.TEAL_A200)

    BlueSkyUIColors = {'top': Color.BLUE_SKY, 'bottom' : Color.INDIGO_500}
    RedUIColors = {'top': Color.RED_500, 'bottom' : Color.BLACK}
    TestUIColors = {'top': Color.LIGHT_BLUE_A200, 'bottom' : Color.BLACK}


# class MaterialDesignColors(Color):

# class MaterialDesignAccentColors(Color):

# class BootstrapColors(Color):