"""Tests for scene-level composition with per-layer sizing."""

import numpy as np

from ledwall_server.plugins.effect import SolidColor
from ledwall_server.renderer import Renderer


def test_per_layer_sizing():
    """Plugin should receive correct w/h from layer config."""
    plugin = SolidColor({"color": [255, 0, 0]}, 16, 8)
    assert plugin.width == 16
    assert plugin.height == 8
    frame = plugin.render()
    assert frame.shape == (8, 16, 3)


def test_dashboard_composition():
    """Dashboard scene should compose layers at correct positions."""
    renderer = Renderer(32, 24)
    # Simulate dashboard: red (16x16), green (16x16), blue (32x8)
    red = SolidColor({"color": [255, 0, 0]}, 16, 16)
    green = SolidColor({"color": [0, 255, 0]}, 16, 16)
    blue = SolidColor({"color": [0, 0, 255]}, 32, 8)
    layers = [(red, 0, 0), (green, 16, 0), (blue, 0, 16)]
    frame = renderer.compose(layers)
    assert frame.shape == (24, 32, 3)
    # Top-left 16x16 = red
    assert np.all(frame[0, 0] == [255, 0, 0])
    assert np.all(frame[15, 15] == [255, 0, 0])
    # Top-right 16x16 = green
    assert np.all(frame[0, 16] == [0, 255, 0])
    assert np.all(frame[15, 31] == [0, 255, 0])
    # Bottom 32x8 = blue
    assert np.all(frame[16, 0] == [0, 0, 255])
    assert np.all(frame[23, 31] == [0, 0, 255])


def test_layers_dont_bleed_outside_bounds():
    """A small plugin placed at an offset should not affect other areas."""
    renderer = Renderer(32, 24)
    small = SolidColor({"color": [255, 255, 0]}, 8, 8)
    layers = [(small, 4, 4)]
    frame = renderer.compose(layers)
    # Inside bounds should be yellow
    assert np.all(frame[4, 4] == [255, 255, 0])
    assert np.all(frame[11, 11] == [255, 255, 0])
    # Outside bounds should be black
    assert np.all(frame[0, 0] == 0)
    assert np.all(frame[3, 3] == 0)
    assert np.all(frame[12, 12] == 0)
    assert np.all(frame[23, 31] == 0)


def test_overlapping_layers_last_wins():
    """Later layers should overwrite earlier ones where both are non-zero."""
    renderer = Renderer(16, 16)
    red = SolidColor({"color": [255, 0, 0]}, 16, 16)
    green = SolidColor({"color": [0, 255, 0]}, 8, 8)
    layers = [(red, 0, 0), (green, 0, 0)]
    frame = renderer.compose(layers)
    # Where green overlaps, green wins
    assert np.all(frame[0, 0] == [0, 255, 0])
    assert np.all(frame[7, 7] == [0, 255, 0])
    # Where only red exists, red remains
    assert np.all(frame[8, 8] == [255, 0, 0])
    assert np.all(frame[15, 15] == [255, 0, 0])


def test_plugin_at_edge_clips_correctly():
    """A plugin placed at the edge should clip without error."""
    renderer = Renderer(16, 16)
    big = SolidColor({"color": [128, 128, 128]}, 16, 16)
    layers = [(big, 8, 8)]
    frame = renderer.compose(layers)
    # Only the overlapping 8x8 region should be filled
    assert np.all(frame[8, 8] == [128, 128, 128])
    assert np.all(frame[15, 15] == [128, 128, 128])
    assert np.all(frame[0, 0] == 0)
    assert np.all(frame[7, 7] == 0)
