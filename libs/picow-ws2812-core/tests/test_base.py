"""test iter_pixels and StaticView rendering"""

import pytest
from picow_ws2812_core.base import Collection, Pixel, StaticView, iter_pixels
from picow_ws2812_core.collections.group import Group
from picow_ws2812_core.objects.char import Char
from tests.conftest import TEST_COLOR

RED = (255, 0, 0)


def test_iter_pixels_object():
    char = Char(char="A", color=TEST_COLOR)
    assert list(iter_pixels(char)) == list(char.pixels)


def test_iter_pixels_nested_collections():
    a, b = Char(char="A", color=TEST_COLOR), Char(char="B", color=RED)
    nested = Group([a, Group([b])])
    assert list(iter_pixels(nested)) == list(a.pixels) + list(b.pixels)


def test_iter_pixels_empty_collection():
    assert list(iter_pixels(Collection())) == []


def test_iter_pixels_invalid_type():
    with pytest.raises(ValueError):
        list(iter_pixels("nope"))  # type: ignore[arg-type]


def test_static_view_grid_renders_nested_and_clips():
    char = Char(char="A", color=RED)
    # 2x2 grid is smaller than the char: out-of-range pixels are ignored
    grid = StaticView(nrows=2, ncols=2, objects=[Group([Group([char])])]).get_grid()
    assert grid.shape == (2, 2, 3)
    expected = {(p.y, p.x): p.color for p in char.pixels if p.y < 2 and p.x < 2}
    for (y, x), color in expected.items():
        assert tuple(grid[y, x]) == color
