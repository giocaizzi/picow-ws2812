"""test pixel module"""

from picow_ws2812_core.base import Pixel


def test_pixel_initialization():
    """test the initialization of a pixel"""
    pixel = Pixel(1, 2, (255, 0, 0))
    assert pixel.x == 1
    assert pixel.y == 2
    assert pixel.color == (255, 0, 0)


def test_pixel_setters():
    """test the setters of a pixel"""
    pixel = Pixel(1, 2, (255, 0, 0))
    pixel.x = 10
    pixel.y = 20
    pixel.color = (0, 255, 0)
    assert pixel.x == 10
    assert pixel.y == 20
    assert pixel.color == (0, 255, 0)


def test_pixel_move():
    """test the movement of a pixel"""
    pixel = Pixel(1, 2, (255, 0, 0))
    pixel.move(5, 5)
    assert pixel.x == 6
    assert pixel.y == 7
