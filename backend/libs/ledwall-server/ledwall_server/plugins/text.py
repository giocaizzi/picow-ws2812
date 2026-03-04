"""Text plugin — static or scrolling text."""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ledwall_server.plugins.base import BasePlugin

_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def _load_font(size: int = 8):
    try:
        return ImageFont.truetype(_FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


class StaticText(BasePlugin):
    """Display static text."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.text = config.get("text", "HELLO")
        self.color = tuple(config.get("color", [255, 255, 255]))

    def render(self) -> np.ndarray:
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = _load_font()
        draw.text((0, 0), self.text, fill=self.color, font=font)
        return np.array(img, dtype=np.uint8)

    def tick(self) -> None:
        pass


class ScrollingText(BasePlugin):
    """Horizontally scrolling text."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.text = config.get("text", "SCROLLING TEXT")
        self.color = tuple(config.get("color", [255, 255, 255]))
        self.speed = config.get("speed", 1)
        self._x_offset = width
        self._text_width = len(self.text) * 6  # approximate

    def render(self) -> np.ndarray:
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = _load_font()
        draw.text((self._x_offset, 0), self.text, fill=self.color, font=font)
        return np.array(img, dtype=np.uint8)

    def tick(self) -> None:
        self._x_offset -= self.speed
        if self._x_offset < -self._text_width:
            self._x_offset = self.width
