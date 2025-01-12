from picow_ws2812_core.base import CHAR_WIDTH


from typing import List, Tuple

from picow_ws2812_core.char import Char


class Text:
    """Text object.

    A Text object is an easy representation of a text.
    It contains the text, the color and a list of chars objects.

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
        """Create a list of Char objects.

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