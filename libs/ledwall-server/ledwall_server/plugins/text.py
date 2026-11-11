"""Text plugin — static or scrolling text."""

import numpy as np

from ledwall_server.plugins.base import BasePlugin
from ledwall_server.plugins.fonts import measure_text, render_text


class StaticText(BasePlugin):
    """Display static text."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.text = config.get("text", "HELLO")
        self.color = tuple(config.get("color", [255, 255, 255]))

    def render(self) -> np.ndarray:
        return render_text(self.text, self.width, self.height, self.color)

    def tick(self) -> None:
        pass


class ScrollingText(BasePlugin):
    """Horizontally scrolling text."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.text = config.get("text", "SCROLLING TEXT")
        self.color = tuple(config.get("color", [255, 255, 255]))
        self.speed = config.get("speed", 1)
        self._text_width, _ = measure_text(self.text)
        self._x_offset = width

    def render(self) -> np.ndarray:
        return render_text(
            self.text, self.width, self.height, self.color, x=self._x_offset
        )

    def tick(self) -> None:
        self._x_offset -= self.speed
        if self._x_offset < -self._text_width:
            self._x_offset = self.width
