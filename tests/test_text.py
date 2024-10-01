"""test text module"""

import pytest
from picow_ledwall.base import Text, Char, Pixel, CHAR_WIDTH, CHAR_HEIGHT
from tests.conftest import TEST_COLOR, TEST_STRINGS


@pytest.mark.parametrize("text", TEST_STRINGS)
def test_text_initialization(text):
    """Test the initialization of a Text object"""
    text_obj = Text(text, TEST_COLOR)

    # check if the text object has the correct attributes
    assert text_obj.text == text
    assert text_obj.color == TEST_COLOR

    # hello has same characters
    assert len(text_obj.chars) == len(text)


@pytest.mark.parametrize("text", TEST_STRINGS)
def test_text_char(text):
    """Test the encoding of a Text object"""
    text_obj = Text(text, TEST_COLOR)

    # each element of chars has the correct attributes
    # inherit from Text init
    for char, strchar in zip(text_obj.chars, text):
        assert isinstance(char, Char)
        assert char.char == strchar
        assert char.color == TEST_COLOR


@pytest.mark.parametrize("text", TEST_STRINGS)
def test_text_pixel(text):
    """Test the encoding of a Text object"""
    text_obj = Text(text, TEST_COLOR)

    for char in text_obj.chars:
        # each char is made of pixels
        assert len(char.pixels) > 0
        for pixel in char.pixels:
            assert isinstance(pixel, Pixel)
            # each pixel has the correct color
            assert pixel.color == TEST_COLOR


def test_text_movement():
    """Test the movement of a Text object"""
    text = Text("HELLO", TEST_COLOR)

    # save initial positions
    initial_positions = [
        (pixel.x, pixel.y) for char in text.chars for pixel in char.pixels
    ]
    # move text
    dx, dy = 1, 1
    text.move(dx, dy)

    for (initial_x, initial_y), char in zip(initial_positions, text.chars):
        print(char.char)
        print("initial_x", initial_x)
        print("initial_y", initial_y)
        for pixel in char.pixels:
            assert pixel.x == initial_x + dx
            assert pixel.y == initial_y + dy
