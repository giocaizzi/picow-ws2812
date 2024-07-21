"""basic alphabet for diplaying text on rgb led panel"""

from typing import Tuple

from picow_ledwall.text.fonts import BASEFONT

# the letters are passed as which pixel to turn on
# the pixel number is calculated from the x, y coordinates

CHAR_WIDTH = 5
CHAR_HEIGHT = 7


def encode_letter(char, x: int = 0, y: int = 0):
    """encode letter as list of pixel numbers that should be turned on

    trasforms letters in (x,y) coordinates of the pixels that should be turned
    on.

    Origin: top left corner
    """
    pixels = []
    # check input
    if char not in BASEFONT:
        raise ValueError(f"Letter {char} not in basefont")
    if len(BASEFONT[char]) != CHAR_HEIGHT:
        raise ValueError(f"Letter {char} has wrong height")
    if len(BASEFONT[char][0]) != CHAR_WIDTH:
        raise ValueError(f"Letter {char} has wrong width")
    # encode
    for dy, rowstring in enumerate(BASEFONT[char]):
        for dx, letter in enumerate(rowstring):
            if letter == "1":
                pixels.append((x + dx, y + dy))
    return pixels


class TextString:
    """Text string to be displayed on the rgb led panel

    Args:
        text (str): text to display
        position (Tuple, optional): position of the text on the panel.
            Defaults to (0, 0).
        color (Tuple, optional): color of the text. Defaults to (255, 255, 255).

    Attributes:
        text (str): text to display
        pixels (list): list of pixels that should be turned on
        position (Tuple): position of the text on the panel
        color (Tuple): color of the text
    """

    def __init__(
        self, text: str, position: Tuple = (0, 0), color: Tuple = (255, 255, 255)
    ):
        """initialize the text string"""
        self.text = text.upper()
        self.pixels = []
        self._position = position
        self._color = color
        self._build_string()

    @property
    def position(self) -> Tuple:
        """position of the text on the panel"""
        return self._position

    @position.setter
    def position(self, value) -> None:
        """set the position of the text on the panel"""
        self._position = value
        self._build_string()

    def __len__(self) -> int:
        """length of the text"""
        return len(self.text) * CHAR_WIDTH

    def _build_string(self):
        """build string from letters"""
        # reset pixels
        self.pixels = []
        # position
        x_offset = 0 + self.position[0]
        y_offset = 0 + self.position[1]
        for letter in self.text:
            self.pixels.append(
                (encode_letter(letter, x=x_offset, y=y_offset), self._color)
            )
            x_offset += CHAR_WIDTH
