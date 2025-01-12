from typing import List, Tuple

from picow_ws2812_core.base import CHAR_WIDTH, BaseObject, Collection
from picow_ws2812_core.objects.char import Char


class Text(Collection):
    """Text string.

    A Text object is an easy representation of a text string.
    It contains the text, the color and a list of chars objects.

    Attributes:
        text (str): text
        color (Tuple[int, int, int]): color
        chars (List[Char]): list of chars
    """

    def __init__(
        self,
        text: str,
        color: Tuple[int, int, int],
        x0: int = 0,
        y0: int = 0,
    ):
        """Create a Text object.

        Create a Text object with a text and a color.
        (x0, y0) is the top left corner of the text.

        Args:
            text (str): text
            x0 (int): x coordinate
            y0 (int): y coordinate
            color (Tuple[int, int, int]): color
        """
        super().__init__()
        self.text = text
        self.color = color

        # all objects of this complex object
        # are Char objects
        self.add_objects(self._create_objects(x0=x0, y0=y0))

    def _create_objects(self, x0: int, y0: int) -> List[BaseObject]:
        """Create a list of Char objects.

        Returns:
            List[Char]: list of Char objects
        """
        chars = []
        for i, char in enumerate(self.text):
            chars.append(
                Char(char=char, color=self.color, x0=x0, y0=y0, char_width_offset=i)
            )
        return chars
