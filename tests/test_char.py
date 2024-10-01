"""test char module"""

import pytest
from picow_ledwall.base import Char, Pixel, CHAR_HEIGHT, CHAR_WIDTH


def test_char_initialization():
    char = Char("A", (255, 0, 0))
    assert char.char == "A"
    assert char.color == (255, 0, 0)
    assert char.width == 5
    assert char.height == 7
    assert isinstance(char.pixels, list)


def test_char_invalid_initialization():
    with pytest.raises(ValueError):
        Char("AB", (255, 0, 0))


def test_char_encoding():
    char = Char("A", (255, 0, 0))
    assert len(char.pixels) > 0
    for pixel in char.pixels:
        assert isinstance(pixel, Pixel)
        assert pixel.color == (255, 0, 0)


def test_char_invalid_char_in_basefont():
    with pytest.raises(ValueError):
        Char("?", (255, 0, 0))
