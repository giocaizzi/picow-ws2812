"""test char module"""

import pytest

from picow_ws2812.core.base import Pixel
from picow_ws2812.core.objects.char import Char

TEST_COLOR = (0, 255, 0)


def test_char_initialization():
    """test the initialization of a char"""
    char = Char("A", TEST_COLOR)
    assert char.char == "A"
    assert char.color == TEST_COLOR
    assert char.width == 5
    assert char.height == 7
    assert isinstance(char.pixels, list)


def test_char_invalid_initialization():
    """test the initialization of a char"""
    with pytest.raises(ValueError):
        Char("AB", TEST_COLOR)


def test_char_encoding():
    char = Char("A", TEST_COLOR)
    assert len(char.pixels) > 0
    for pixel in char.pixels:
        assert isinstance(pixel, Pixel)
        assert pixel.color == TEST_COLOR
