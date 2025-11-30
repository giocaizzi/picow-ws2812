from typing import Optional, Tuple

from picow_ws2812_core.base import CHAR_HEIGHT, CHAR_WIDTH, BaseObject, Pixel
from picow_ws2812_core.fonts import BASEFONT


class Char(BaseObject):
    """Char object.

    A Char object is a representation of a single character in
    a string. A list of chars is used to create a text object.

    Attributes:
        char (str): character
        color (Tuple[int, int, int]): color
        width (int): width of character
        height (int): height of character
    """

    def __init__(
        self,
        char: str,
        color: Tuple[int, int, int],
        x0: int = 0,
        y0: int = 0,
        char_width_offset: Optional[int] = None,
    ):
        """Create a Char object.

        Create a Char object with a character and a color.

        Args:
            char (str): character
            color (Tuple[int, int, int]): color
            char_width_offset (int): x-offset for the char, so to compose
                chars into a text. This is intended as a integer multiple of
                default `CHAR_WIDTH`. Default is None.

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
        self._create_pixels(x0, y0)

        # if char_width_offset is not None, move the char
        # to the right so to compose chars into a text
        if char_width_offset is not None:
            if not isinstance(char_width_offset, int):
                raise ValueError("Char width offset must be an integer")
            if char_width_offset < 0:
                raise ValueError("Char width offset must be positive")
            else:
                for pixel in self.pixels:
                    pixel.x += char_width_offset * CHAR_WIDTH

    def _create_pixels(self, x0: int, y0: int) -> None:
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
                    self.add_pixel(Pixel(x0 + dx, y0 + dy, self.color))
