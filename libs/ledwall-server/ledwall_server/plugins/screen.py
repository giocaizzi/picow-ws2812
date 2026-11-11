"""Screen system for multi-view plugin composition.

A Screen is a named layout of elements. A plugin can have multiple screens
and use ScreenManager to handle transitions (fixed, auto-cycle, scroll).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ledwall_server.plugins.elements import Element


class Screen:
    """A named layout of elements within a plugin."""

    def __init__(self, name: str, elements: list[Element]):
        self.name = name
        self.elements = elements

    def render(self, width: int, height: int) -> np.ndarray:
        """Render all elements onto a fresh canvas."""
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        for element in self.elements:
            element.draw(canvas)
        return canvas


class ScreenManager:
    """Manages multiple screens with transition logic.

    Modes:
        fixed: Always shows the first screen.
        auto: Cycles through screens at a configurable interval.
        scroll: Horizontally scrolls between screens.
    """

    def __init__(
        self,
        screens: list[Screen],
        mode: str = "fixed",
        interval: int = 90,
    ):
        """
        Args:
            screens: Ordered list of screens.
            mode: "fixed", "auto", or "scroll".
            interval: Frames between auto transitions (90 frames = 3s at 30fps).
        """
        self.screens = screens
        self.mode = mode
        self.interval = interval
        self._current = 0
        self._timer = 0
        self._scroll_offset = 0

    @property
    def current_index(self) -> int:
        return self._current

    def tick(self) -> None:
        """Advance transition state by one frame."""
        if len(self.screens) <= 1:
            return
        if self.mode == "auto":
            self._timer += 1
            if self._timer >= self.interval:
                self._timer = 0
                self._current = (self._current + 1) % len(self.screens)
        elif self.mode == "scroll":
            self._scroll_offset += 1

    def render(self, width: int, height: int) -> np.ndarray:
        """Render current screen (or scrolling transition)."""
        if not self.screens:
            return np.zeros((height, width, 3), dtype=np.uint8)
        if self.mode in ("fixed", "auto"):
            return self.screens[self._current].render(width, height)
        if self.mode == "scroll":
            return self._render_scroll(width, height)
        return self.screens[self._current].render(width, height)

    def _render_scroll(self, width: int, height: int) -> np.ndarray:
        """Render horizontal scroll transition between screens."""
        curr = self.screens[self._current].render(width, height)
        next_idx = (self._current + 1) % len(self.screens)
        nxt = self.screens[next_idx].render(width, height)
        offset = self._scroll_offset % width
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        # Current screen scrolls left, next enters from right
        canvas[:, : width - offset] = curr[:, offset:]
        canvas[:, width - offset :] = nxt[:, :offset]
        if offset == 0 and self._scroll_offset > 0:
            self._current = next_idx
            self._scroll_offset = 0
        return canvas
