"""test LedWall._show_view with a stubbed neopixel (no MicroPython needed)"""

import sys
import types

import pytest
from picow_ws2812_core.base import StaticSequence, StaticView
from picow_ws2812_core.collections.group import Group
from picow_ws2812_core.objects.char import Char


class FakeNeopixel:
    def __init__(self, *args, **kwargs):
        self.pixels = {}
        self.calls = []

    def brightness(self, value):
        pass

    def set_pixel(self, n, color):
        self.pixels[n] = color

    def show(self):
        self.calls.append("show")

    def clear(self):
        self.calls.append("clear")


@pytest.fixture
def ledwall_cls(monkeypatch):
    stub = types.ModuleType("picow_ws2812_driver.neopixel")
    stub.Neopixel = FakeNeopixel  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "picow_ws2812_driver.neopixel", stub)
    monkeypatch.delitem(sys.modules, "picow_ws2812_driver.ledwall", raising=False)
    from picow_ws2812_driver.ledwall import LedWall

    return LedWall


def test_show_view_renders_objects_and_collections(ledwall_cls):
    wall = ledwall_cls(8, 32, 28)
    wall.wait = 0
    char = Char(char="A", color=(1, 2, 3))
    view = StaticView(nrows=8, ncols=32, objects=[Group([char])])
    wall.display(StaticSequence([view]))

    expected = {
        wall.indexer.get_pixel_number(p.x, p.y): p.color
        for p in char.pixels
        if 0 <= p.x < 32 and 0 <= p.y < 8
    }
    assert wall.pixels == expected and expected
    assert wall.calls == ["show", "clear"]


def test_show_view_ignores_out_of_range_pixels(ledwall_cls):
    wall = ledwall_cls(8, 32, 28)
    wall.wait = 0
    char = Char(char="A", color=(1, 2, 3), x0=1000, y0=1000)

    def raising(n, color):
        raise IndexError

    wall.set_pixel = raising
    wall._show_view(StaticView(nrows=8, ncols=32, objects=[char]))
    assert wall.calls == ["show", "clear"]
