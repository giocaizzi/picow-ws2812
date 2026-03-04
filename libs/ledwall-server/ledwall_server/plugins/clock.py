"""Clock widget plugin — displays current time."""

from datetime import datetime

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ledwall_server.plugins.base import BasePlugin

_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def _load_font(size: int = 8):
    try:
        return ImageFont.truetype(_FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


class Clock(BasePlugin):
    """Display the current time as HH:MM."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.color = tuple(config.get("color", [255, 255, 255]))
        self._time_str = ""

    def render(self) -> np.ndarray:
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = _load_font()
        draw.text((0, 0), self._time_str, fill=self.color, font=font)
        return np.array(img, dtype=np.uint8)

    def tick(self) -> None:
        self._time_str = datetime.now().strftime("%H:%M")
