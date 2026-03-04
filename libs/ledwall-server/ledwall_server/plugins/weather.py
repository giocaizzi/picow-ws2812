"""Weather plugin — displays temperature from an API.

Placeholder implementation; requires external API key configuration.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ledwall_server.plugins.base import BasePlugin

_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def _load_font(size: int = 8):
    try:
        return ImageFont.truetype(_FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


class Weather(BasePlugin):
    """Display weather information."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.color = tuple(config.get("color", [255, 255, 255]))
        self._text = config.get("text", "22°C")

    def render(self) -> np.ndarray:
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = _load_font()
        draw.text((0, 0), self._text, fill=self.color, font=font)
        return np.array(img, dtype=np.uint8)

    def tick(self) -> None:
        # TODO: Fetch weather data from API periodically
        pass
