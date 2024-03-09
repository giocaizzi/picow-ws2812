"""basic alphabet for diplaying text on rgb led panel"""

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
                pixels.append((x + dx, x + dy))
    return pixels


class TextString:
    """Text string to be displayed on the rgb led panel"""

    def __init__(self, text, ledwall):
        self.text = text
        self.ledwall = ledwall
        self.encoded_text = []

    def _build_string(self):
        """build string from letters"""
        x_offset = 0
        for letter in self.text:
            self.encoded_text.append(encode_letter(letter, x_offset))
            x_offset += CHAR_WIDTH

    def display(self, x, color):
        """display the text on the ledwall"""
        self._build_string()
        for letter in self.encoded_text:
            for x, y in letter:
                self.ledwall.set_pixel(self.ledwall.indexer.get_pixel_number(x, y), color)
        self.ledwall.show()
