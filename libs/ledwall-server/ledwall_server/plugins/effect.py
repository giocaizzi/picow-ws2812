"""Generative effects plugin — rainbow, color cycle, etc."""

import numpy as np

from ledwall_server.plugins.base import BasePlugin


class SolidColor(BasePlugin):
    """Fill the display with a single color."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.color = config.get("color", [255, 0, 0])

    def render(self) -> np.ndarray:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame[:] = self.color
        return frame

    def tick(self) -> None:
        pass


class ColorCycle(BasePlugin):
    """Cycle through hue values across the display."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.hue_offset = 0
        self.speed = config.get("speed", 5)

    def render(self) -> np.ndarray:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for x in range(self.width):
            hue = (self.hue_offset + x * 8) % 360
            r, g, b = self._hsv_to_rgb(hue, 1.0, 1.0)
            frame[:, x] = [r, g, b]
        return frame

    def tick(self) -> None:
        self.hue_offset = (self.hue_offset + self.speed) % 360

    @staticmethod
    def _hsv_to_rgb(h: float, s: float, v: float) -> tuple[int, int, int]:
        """Convert HSV (h in 0-360, s/v in 0-1) to RGB (0-255)."""
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        if h < 60:
            r, g, b = c, x, 0
        elif h < 120:
            r, g, b = x, c, 0
        elif h < 180:
            r, g, b = 0, c, x
        elif h < 240:
            r, g, b = 0, x, c
        elif h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        return int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)


class Rainbow(BasePlugin):
    """Diagonal rainbow sweep."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.offset = 0
        self.speed = config.get("speed", 3)

    def render(self) -> np.ndarray:
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for y in range(self.height):
            for x in range(self.width):
                hue = (self.offset + x * 6 + y * 6) % 360
                frame[y, x] = ColorCycle._hsv_to_rgb(hue, 1.0, 1.0)
        return frame

    def tick(self) -> None:
        self.offset = (self.offset + self.speed) % 360
