"""Base plugin interface for LED wall server."""

from abc import ABC, abstractmethod

import numpy as np


class BasePlugin(ABC):
    """Abstract base class for all display plugins.

    Each plugin renders to its own (height, width, 3) numpy array.
    The compositor layers them together.
    """

    def __init__(self, config: dict, width: int, height: int):
        self.config = config
        self.width = width
        self.height = height

    @abstractmethod
    def render(self) -> np.ndarray:
        """Return a (height, width, 3) uint8 RGB array."""

    @abstractmethod
    def tick(self) -> None:
        """Advance animation state by one frame."""
