"""Tests for the frame renderer/compositor."""

import numpy as np

from ledwall_server.plugins.effect import ColorCycle, SolidColor
from ledwall_server.renderer import Renderer


def test_renderer_empty():
    """Composing no layers returns black frame."""
    r = Renderer(32, 24)
    frame = r.compose([])
    assert frame.shape == (24, 32, 3)
    assert np.all(frame == 0)


def test_renderer_solid_color():
    """Single solid color plugin fills the frame."""
    r = Renderer(32, 24)
    plugin = SolidColor({"color": [255, 0, 0]}, 32, 24)
    frame = r.compose([(plugin, 0, 0)])
    assert frame.shape == (24, 32, 3)
    assert np.all(frame[:, :, 0] == 255)
    assert np.all(frame[:, :, 1] == 0)
    assert np.all(frame[:, :, 2] == 0)


def test_renderer_overlay():
    """A second layer overwrites the first where non-black."""
    r = Renderer(32, 24)
    red = SolidColor({"color": [255, 0, 0]}, 32, 24)
    green = SolidColor({"color": [0, 255, 0]}, 16, 12)
    frame = r.compose([(red, 0, 0), (green, 0, 0)])
    # Top-left 12x16 should be green
    assert np.all(frame[0, 0] == [0, 255, 0])
    # Bottom-right should remain red
    assert np.all(frame[23, 31] == [255, 0, 0])


def test_color_cycle_produces_different_frames():
    """ColorCycle plugin should produce changing frames over time."""
    plugin = ColorCycle({"speed": 30}, 32, 24)
    frame1 = plugin.render().copy()
    plugin.tick()
    frame2 = plugin.render()
    assert not np.array_equal(frame1, frame2)
