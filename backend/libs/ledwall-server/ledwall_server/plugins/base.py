"""Base plugin interface for LED wall server."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ledwall_server.plugins.screen import ScreenManager


class BasePlugin(ABC):
    """Abstract base class for all display plugins.

    Each plugin renders to its own (height, width, 3) numpy array.
    The compositor layers them together.

    Plugins can either:
    - Override render()/tick() directly (simple plugins, backward compatible)
    - Use ScreenManager for multi-screen composition
    """

    def __init__(self, config: dict, width: int, height: int):
        self.config = config
        self.width = width
        self.height = height
        self.screen_manager: ScreenManager | None = None

    def render(self) -> np.ndarray:
        """Return a (height, width, 3) uint8 RGB array.

        Default: delegate to screen_manager if set.
        """
        if self.screen_manager:
            return self.screen_manager.render(self.width, self.height)
        return np.zeros((self.height, self.width, 3), dtype=np.uint8)

    @abstractmethod
    def tick(self) -> None:
        """Advance animation state by one frame."""
