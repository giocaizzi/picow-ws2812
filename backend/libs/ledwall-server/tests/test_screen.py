"""Tests for Screen and ScreenManager."""

import numpy as np

from ledwall_server.plugins.elements import RectElement
from ledwall_server.plugins.screen import Screen, ScreenManager


def _make_screen(name: str, color: tuple[int, int, int]) -> Screen:
    """Helper to create a screen with a single filled rect."""
    return Screen(name, [RectElement(0, 0, 8, 8, color=color)])


def test_screen_renders_all_elements():
    """Screen should render all its elements onto the canvas."""
    screen = Screen(
        "test",
        [
            RectElement(0, 0, 4, 4, color=(255, 0, 0)),
            RectElement(4, 4, 4, 4, color=(0, 255, 0)),
        ],
    )
    canvas = screen.render(8, 8)
    assert canvas.shape == (8, 8, 3)
    assert np.all(canvas[0, 0] == [255, 0, 0])
    assert np.all(canvas[4, 4] == [0, 255, 0])


def test_screen_manager_fixed_stays_on_first():
    """Fixed mode should always show the first screen."""
    s1 = _make_screen("a", (255, 0, 0))
    s2 = _make_screen("b", (0, 255, 0))
    mgr = ScreenManager([s1, s2], mode="fixed")
    for _ in range(100):
        mgr.tick()
    assert mgr.current_index == 0
    canvas = mgr.render(8, 8)
    assert np.all(canvas[0, 0] == [255, 0, 0])


def test_screen_manager_auto_cycles():
    """Auto mode should cycle to next screen after interval frames."""
    s1 = _make_screen("a", (255, 0, 0))
    s2 = _make_screen("b", (0, 255, 0))
    mgr = ScreenManager([s1, s2], mode="auto", interval=10)
    assert mgr.current_index == 0
    for _ in range(10):
        mgr.tick()
    assert mgr.current_index == 1
    canvas = mgr.render(8, 8)
    assert np.all(canvas[0, 0] == [0, 255, 0])


def test_screen_manager_auto_wraps():
    """Auto mode should wrap around to first screen."""
    s1 = _make_screen("a", (255, 0, 0))
    s2 = _make_screen("b", (0, 255, 0))
    mgr = ScreenManager([s1, s2], mode="auto", interval=5)
    for _ in range(10):
        mgr.tick()
    assert mgr.current_index == 0


def test_screen_manager_scroll_transitions():
    """Scroll mode should produce a blended frame during transition."""
    s1 = _make_screen("a", (255, 0, 0))
    s2 = _make_screen("b", (0, 255, 0))
    mgr = ScreenManager([s1, s2], mode="scroll")
    # Initial render should be screen 1
    canvas = mgr.render(8, 8)
    assert np.all(canvas[0, 0] == [255, 0, 0])
    # After some ticks, should start showing screen 2 on the right
    for _ in range(4):
        mgr.tick()
    canvas = mgr.render(8, 8)
    # Right edge should now have screen 2 pixels
    assert np.all(canvas[0, 7] == [0, 255, 0])


def test_screen_manager_single_screen():
    """Single screen should not change regardless of mode."""
    s1 = _make_screen("only", (255, 0, 0))
    for mode in ("fixed", "auto", "scroll"):
        mgr = ScreenManager([s1], mode=mode, interval=5)
        for _ in range(20):
            mgr.tick()
        assert mgr.current_index == 0


def test_screen_manager_empty_screens():
    """Empty screens list should render black."""
    mgr = ScreenManager([], mode="auto")
    canvas = mgr.render(8, 8)
    assert canvas.shape == (8, 8, 3)
    assert np.all(canvas == 0)
