"""Tests for visual elements."""

import numpy as np

from ledwall_server.plugins.elements import (
    BarElement,
    IconElement,
    RectElement,
    TextElement,
)


def test_text_element_draws_nonzero_pixels():
    """TextElement should draw text pixels onto the canvas."""
    canvas = np.zeros((16, 32, 3), dtype=np.uint8)
    elem = TextElement(0, 0, 32, 16, text="A", color=(255, 255, 255))
    elem.draw(canvas)
    assert np.any(canvas > 0), "TextElement should draw visible pixels"


def test_text_element_empty_string():
    """TextElement with empty text should not modify canvas."""
    canvas = np.zeros((8, 16, 3), dtype=np.uint8)
    elem = TextElement(0, 0, 16, 8, text="", color=(255, 0, 0))
    elem.draw(canvas)
    assert np.all(canvas == 0)


def test_text_element_color():
    """TextElement should draw in the specified color."""
    canvas = np.zeros((16, 32, 3), dtype=np.uint8)
    elem = TextElement(0, 0, 32, 16, text="X", color=(255, 0, 0))
    elem.draw(canvas)
    # All non-zero pixels should be red
    mask = np.any(canvas > 0, axis=2)
    if np.any(mask):
        assert np.all(canvas[mask][:, 0] > 0), "Red channel should be active"


def test_icon_element_draws_bitmap():
    """IconElement should draw the icon bitmap onto the canvas."""
    canvas = np.zeros((8, 8, 3), dtype=np.uint8)
    elem = IconElement(0, 0, 8, 8, icon="sun", color=(255, 200, 0))
    elem.draw(canvas)
    assert np.any(canvas > 0), "IconElement should draw visible pixels"


def test_icon_element_unknown_icon():
    """IconElement with unknown icon should not draw anything."""
    canvas = np.zeros((8, 8, 3), dtype=np.uint8)
    elem = IconElement(0, 0, 8, 8, icon="nonexistent", color=(255, 0, 0))
    elem.draw(canvas)
    assert np.all(canvas == 0)


def test_icon_element_correct_color():
    """IconElement should draw pixels in the specified color."""
    canvas = np.zeros((8, 8, 3), dtype=np.uint8)
    color = (0, 255, 0)
    elem = IconElement(0, 0, 8, 8, icon="drop", color=color)
    elem.draw(canvas)
    mask = np.any(canvas > 0, axis=2)
    assert np.any(mask)
    assert np.all(canvas[mask] == list(color))


def test_rect_element_filled():
    """RectElement with fill=True should fill the entire area."""
    canvas = np.zeros((10, 10, 3), dtype=np.uint8)
    elem = RectElement(2, 2, 4, 4, color=(255, 0, 0), fill=True)
    elem.draw(canvas)
    # Check filled region
    assert np.all(canvas[2:6, 2:6, 0] == 255)
    assert np.all(canvas[2:6, 2:6, 1] == 0)
    # Check outside is still black
    assert np.all(canvas[0, 0] == 0)


def test_rect_element_outline():
    """RectElement with fill=False should only draw border pixels."""
    canvas = np.zeros((10, 10, 3), dtype=np.uint8)
    elem = RectElement(1, 1, 5, 5, color=(0, 0, 255), fill=False)
    elem.draw(canvas)
    # Top-left corner should be drawn
    assert np.all(canvas[1, 1] == [0, 0, 255])
    # Interior should be black
    assert np.all(canvas[3, 3] == 0)
    # Bottom-right corner should be drawn
    assert np.all(canvas[5, 5] == [0, 0, 255])


def test_bar_element_draws_at_proportion():
    """BarElement should fill proportionally to value."""
    canvas = np.zeros((4, 10, 3), dtype=np.uint8)
    elem = BarElement(0, 0, 10, 4, value=0.5, color=(0, 255, 0), bg=(30, 30, 30))
    elem.draw(canvas)
    # First 5 columns should be green
    assert np.all(canvas[0, 0] == [0, 255, 0])
    assert np.all(canvas[0, 4] == [0, 255, 0])
    # Columns 5-9 should be background
    assert np.all(canvas[0, 5] == [30, 30, 30])
    assert np.all(canvas[0, 9] == [30, 30, 30])


def test_bar_element_zero_value():
    """BarElement with value=0 should show all background."""
    canvas = np.zeros((2, 8, 3), dtype=np.uint8)
    elem = BarElement(0, 0, 8, 2, value=0.0, color=(255, 0, 0), bg=(10, 10, 10))
    elem.draw(canvas)
    assert np.all(canvas[:2, :8] == [10, 10, 10])


def test_bar_element_full_value():
    """BarElement with value=1.0 should be fully colored."""
    canvas = np.zeros((2, 8, 3), dtype=np.uint8)
    elem = BarElement(0, 0, 8, 2, value=1.0, color=(255, 0, 0), bg=(10, 10, 10))
    elem.draw(canvas)
    assert np.all(canvas[:2, :8, 0] == 255)


def test_bar_element_clamps_value():
    """BarElement should clamp value to [0, 1]."""
    elem = BarElement(0, 0, 8, 2, value=1.5)
    assert elem.value == 1.0
    elem2 = BarElement(0, 0, 8, 2, value=-0.5)
    assert elem2.value == 0.0
