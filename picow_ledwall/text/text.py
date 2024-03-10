"""basic alphabet for diplaying text on rgb led panel"""

import time
from picow_ledwall.text.fonts import BASEFONT

# the letters are passed as which pixel to turn on
# the pixel number is calculated from the x, y coordinates

CHAR_WIDTH = 5
CHAR_HEIGHT = 7


def encode_letter(char, x=0, y=0):
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
    """Text string to be displayed on the rgb led panel"""

    def __init__(self, text, position=(0, 0), color=(255, 255, 255)):
        self.text = text.upper()
        self.pixels = []
        self._position = position
        self._color = color
        self._build_string()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value
        self._build_string()

    def _build_string(self):
        """build string from letters"""
        # reset pixels
        self.pixels = []
        # position
        x_offset = 0 + self.position[0]
        for letter in self.text:
            self.pixels.append((encode_letter(letter, x=x_offset), self._color))
            x_offset += CHAR_WIDTH
