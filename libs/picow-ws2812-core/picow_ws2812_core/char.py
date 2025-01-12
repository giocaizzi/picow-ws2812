from picow_ws2812_core.base import CHAR_HEIGHT, CHAR_WIDTH, Object, Pixel
from picow_ws2812_core.fonts import BASEFONT


from typing import Tuple


class Char(Object):
    """Char object.

    A Char object is a representation of a single character.
    It contains the character, the color and a list of pixels.

    Attributes:
        char (str): character
        color (Tuple[int, int, int]): color
        width (int): width of character
        height (int): height of character
    """

    def __init__(self, char: str, color: Tuple[int, int, int]):
        """Create a Char object.

        Create a Char object with a character and a color.

        Args:
            char (str): character
            color (Tuple[int, int, int]): color

        Raises:
            ValueError: if char is not a single character
        """
        if len(char) > 1:
            raise ValueError("Char must be a single character")

        self.char = char.upper()
        self.color = color
        super().__init__()

        # dimensions of the char
        self.width = CHAR_WIDTH
        self.height = CHAR_HEIGHT

        # create pixes
        self._create_pixels()

    def _create_pixels(self) -> None:
        """Encode char to Pixel.

        Reads the font from the pixel font
        and creates a list of pixels.

        Raises:
            ValueError: if char not in basefont
            ValueError: if char has wrong height
            ValueError: if char has wrong width
        """

        if self.char not in BASEFONT:
            raise ValueError(f"Letter {self.char} not in basefont")
        if len(BASEFONT[self.char]) != self.height:
            raise ValueError(f"Letter {self.char} has wrong height")
        if len(BASEFONT[self.char][0]) != self.width:
            raise ValueError(f"Letter {self.char} has wrong width")

        for dy, rowstring in enumerate(BASEFONT[self.char]):
            for dx, letter in enumerate(rowstring):
                if letter == "1":
                    self.add_pixel(Pixel(dx, dy, self.color))