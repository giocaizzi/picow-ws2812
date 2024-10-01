"""test text module"""

import pytest
from picow_ledwall.base import Text, Char, Pixel, CHAR_WIDTH, CHAR_HEIGHT


TEST_COLOR = (0, 255, 0)
TEST_STRINGS = [
    "HELLO",
    "ciao",
    "12345",
    "ciao1w323vS",
    "BAGUS!",
    # TODO: implement `?`
    # "WHY???",
]


@pytest.mark.parametrize("text", TEST_STRINGS)
def test_text_initialization(text):
    """Test the initialization of a Text object"""
    text_obj = Text(text, TEST_COLOR)

    # check if the text object has the correct attributes
    assert text_obj.text == text
    assert text_obj.color == TEST_COLOR

    # hello has same characters
    assert len(text_obj.chars) == len(text)

    for char in text_obj.chars:
        assert isinstance(char, Char)
        assert char.color == TEST_COLOR


@pytest.mark.parametrize("text", TEST_STRINGS)
def test_text_encoding(text):
    """Test the encoding of a Text object"""
    text_obj = Text(text, TEST_COLOR)

    assert len(text_obj.chars) == len(text)

    for char in text_obj.chars:
        # each char is made of pixels
        assert len(char.pixels) > 0
        for pixel in char.pixels:
            assert isinstance(pixel, Pixel)
            # each pixel has the correct color
            assert pixel.color == TEST_COLOR


def test_text_movement():
    text = Text("HELLO", TEST_COLOR)
    initial_positions = [
        (pixel.x, pixel.y) for char in text.chars for pixel in char.pixels
    ]
    text.move(1, 1)
    for (initial_x, initial_y), char in zip(initial_positions, text.chars):
        for pixel in char.pixels:
            assert pixel.x == initial_x + 1
            assert pixel.y == initial_y + 1
