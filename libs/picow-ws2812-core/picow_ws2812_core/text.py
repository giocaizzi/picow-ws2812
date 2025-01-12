from picow_ws2812_core.base import CHAR_WIDTH


from typing import List, Tuple

from picow_ws2812_core.base import ComplexObject
from picow_ws2812_core.char import Char


class Text(ComplexObject):
    """Text string.

    A Text object is an easy representation of a text string.
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
        super().__init__()
        self.text = text
        self.color = color

        # all objects of this complex object
        # are Char objects
        for char in self._create_objects():
            self.add_object(char)

    def _create_objects(self) -> List[Char]:
        """Create a list of Char objects.

        Returns:
            List[Char]: list of Char objects
        """
        chars = []
        for i, char in enumerate(self.text):
            chars.append(Char(char, self.color, char_width_offset=i))
        return chars
