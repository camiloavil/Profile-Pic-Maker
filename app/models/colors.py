from enum import Enum

class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BROWN = (139, 69, 19)
    BROWNDARK = (77, 77, 80)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    BLUE_SKY = (135, 206, 250)   # Azul claro
    TURQUOISE = (26, 188, 156)
    EMERALD = (46, 204, 113)
    WET_ASPHALT = (52, 73, 94)
    GREEN_SEA = (22, 160, 133)
    NEPHRITIS = (39, 174, 73)
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
    LIGHT = (248, 249, 250)
    DARK = (52, 58, 64)
    ORANGE = (255, 127, 39)
    ORANGE_CARROT = (255, 165, 0)
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

    def get_color_rgb(color_name: str) -> tuple:
        try:
            # Look up the color in the Color enum (case insensitive)
            return getattr(Color, color_name.upper())
        except AttributeError:
            raise ValueError(f'Invalid color name: {color_name}')
        # return Color.BLACK.value
    
    @staticmethod
    def print_all_names():
        """Print the names of all members in the Color enum."""
        for color in Color:
            print(color.name)

class Colors(Enum):
    BLUE_SKY_TO_INDIGO = (Color.BLUE_SKY, Color.INDIGO_500)
    BLUE_WHITE_CLEAN = (Color.BLUE_SKY, Color.WHITE)
    BLUE_BLACK_CLEAN = (Color.BLUE_SKY, Color.BLACK)
    ORANGE_BLACK_CLEAN = (Color.ORANGE, Color.BLACK)
    RED_TO_BLACK_CLEAN = (Color.RED_500, Color.BLACK)
    BROWN_TO_BLACK_CLEAN = (Color.BROWN, Color.BLACK)
    BROWN_TO_WHITE_CLEAN = (Color.BROWN, Color.WHITE)
    WHITE_TO_BROWNDARK_CLEAN = (Color.WHITE, Color.BROWNDARK)
    LIGHT_BLUE_A200_TO_BLACK = (Color.LIGHT_BLUE_A200, Color.BLACK)

