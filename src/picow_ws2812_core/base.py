"""base classes."""

from typing import Tuple, List
from picow_ws2812_core.fonts import BASEFONT

CHAR_WIDTH = 5
CHAR_HEIGHT = 7


class Pixel:
    """Pixel object.

    A Pixel object is a representation of a single pixel
    in the ledwall.

    Attributes:
        x (int): x position
        y (int): y position
        color (Tuple[int, int, int]): color
    """

    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        """Create a Pixel object.

        Create a Pixel object with an x and y position and a color.

        Args:
            x (int): x position
            y (int): y position
            color (Tuple[int, int, int]): color
        """
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self) -> int:
        """Return x position of pixel."""
        return self._x

    @x.setter
    def x(self, x: int):
        """Set x position of pixel.

        Args:
            x (int): x position
        """
        self._x = x

    @property
    def y(self) -> int:
        """Return y position of pixel."""
        return self._y

    @y.setter
    def y(self, y: int):
        """Set y position of pixel.

        Args:
            y (int): y position
        """
        self._y = y

    @property
    def color(self) -> Tuple[int, int, int]:
        """Return color of pixel."""
        return self._color

    @color.setter
    def color(self, color: Tuple[int, int, int]):
        """Set color of pixel.

        Args:
            color (Tuple[int, int, int]): color
        """
        self._color = color

    def move(self, dx: int, dy: int) -> None:
        """Move pixel."""
        self.x += dx
        self.y += dy


class Char:
    """Char object.

    A Char object is a representation of a single character.
    It contains the character, the color and a list of pixels.

    Attributes:
        char (str): character
        color (Tuple[int, int, int]): color
        pixels (List[Pixel]): list of pixels
        width (int): width of character
        height (int): height of character
    """

    pixels: List[Pixel] = []

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
        self.pixels = []  # Initialize pixels list

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
                    self.pixels.append(Pixel(dx, dy, self.color))


class Text:
    """Text object.

    A Text object is a representation of a text.
    It contains the text, the color and a list of chars.

    Attributes:
        text (str): text
        color (Tuple[int, int, int]): color
        chars (List[Char]): list of chars
    """

    def __init__(self, text: str, color: Tuple[int, int, int]):
        """Create a Text object.

        Create a Text object with a text and a color.

        Args:
            text (str): text
            color (Tuple[int, int, int]): color
        """
        self.text = text
        self.color = color
        self.chars = self._create_chars()

    def _create_chars(self) -> List[Char]:
        """Create a list of letters.

        Returns:
            List[Char]: list of Char objects
        """
        chars = []
        for i, char in enumerate(self.text):
            chars.append(Char(char, self.color))
            for pixel in chars[i].pixels:
                pixel.x += i * CHAR_WIDTH
        return chars

    def move(self, dx: int, dy: int):
        """Move text.

        Move the text by dx and dy.

        Args:
            dx (int): x movement
            dy (int): y movement
        """
        for char in self.chars:
            for pixel in char.pixels:
                pixel.move(dx, dy)
