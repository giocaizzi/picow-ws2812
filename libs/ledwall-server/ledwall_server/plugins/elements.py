"""Visual building blocks for composing plugin screens.

Elements are small, reusable renderers that draw onto a numpy subregion.
They don't tick or manage state — they just draw.
"""

from abc import ABC, abstractmethod

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ledwall_server.plugins.icons import IconSize, get_icon

_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def _load_font(size: int = 8) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        return ImageFont.truetype(_FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


class Element(ABC):
    """A visual building block that renders onto a numpy array."""

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    @abstractmethod
    def draw(self, canvas: np.ndarray) -> None:
        """Draw this element onto the canvas in-place."""


class TextElement(Element):
    """Renders text using PIL."""

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        text: str = "",
        color: tuple[int, int, int] = (255, 255, 255),
        font_size: int = 8,
    ):
        super().__init__(x, y, w, h)
        self.text = text
        self.color = color
        self.font_size = font_size

    def draw(self, canvas: np.ndarray) -> None:
        if not self.text:
            return
        img = Image.new("RGB", (self.w, self.h), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = _load_font(self.font_size)
        draw.text((0, 0), self.text, fill=self.color, font=font)
        rendered = np.array(img, dtype=np.uint8)
        self._blit(canvas, rendered)

    def _blit(self, canvas: np.ndarray, rendered: np.ndarray) -> None:
        """Copy non-zero pixels from rendered onto canvas at (self.x, self.y)."""
        ch, cw = canvas.shape[:2]
        rh, rw = rendered.shape[:2]
        # Compute clipped region
        sy0 = max(0, -self.y)
        sx0 = max(0, -self.x)
        dy0 = max(0, self.y)
        dx0 = max(0, self.x)
        h = min(rh - sy0, ch - dy0)
        w = min(rw - sx0, cw - dx0)
        if h <= 0 or w <= 0:
            return
        src = rendered[sy0 : sy0 + h, sx0 : sx0 + w]
        mask = np.any(src > 0, axis=2)
        canvas[dy0 : dy0 + h, dx0 : dx0 + w][mask] = src[mask]


class IconElement(Element):
    """Renders a small bitmap icon from the built-in icon set."""

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        icon: str = "",
        color: tuple[int, int, int] = (255, 255, 255),
        icon_size: IconSize = IconSize.L,
    ):
        super().__init__(x, y, w, h)
        self.icon = icon
        self.color = color
        self.icon_size = icon_size

    def draw(self, canvas: np.ndarray) -> None:
        bitmap = get_icon(self.icon, self.icon_size)
        if bitmap is None:
            return
        ch, cw = canvas.shape[:2]
        icon_h = len(bitmap)
        icon_w = len(bitmap[0]) if bitmap else 0
        for iy in range(min(icon_h, self.h)):
            for ix in range(min(icon_w, self.w)):
                if bitmap[iy][ix] == "1":
                    py = self.y + iy
                    px = self.x + ix
                    if 0 <= py < ch and 0 <= px < cw:
                        canvas[py, px] = self.color


class RectElement(Element):
    """Filled or outlined rectangle."""

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        color: tuple[int, int, int] = (255, 255, 255),
        fill: bool = True,
    ):
        super().__init__(x, y, w, h)
        self.color = color
        self.fill = fill

    def draw(self, canvas: np.ndarray) -> None:
        ch, cw = canvas.shape[:2]
        for iy in range(self.h):
            for ix in range(self.w):
                py = self.y + iy
                px = self.x + ix
                if not (0 <= py < ch and 0 <= px < cw):
                    continue
                if (
                    self.fill
                    or iy == 0
                    or iy == self.h - 1
                    or ix == 0
                    or ix == self.w - 1
                ):
                    canvas[py, px] = self.color


class BarElement(Element):
    """Horizontal progress bar."""

    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        value: float = 0.0,
        color: tuple[int, int, int] = (0, 255, 0),
        bg: tuple[int, int, int] = (30, 30, 30),
    ):
        super().__init__(x, y, w, h)
        self.value = max(0.0, min(1.0, value))
        self.color = color
        self.bg = bg

    def draw(self, canvas: np.ndarray) -> None:
        ch, cw = canvas.shape[:2]
        fill_w = int(self.w * self.value)
        for iy in range(self.h):
            for ix in range(self.w):
                py = self.y + iy
                px = self.x + ix
                if 0 <= py < ch and 0 <= px < cw:
                    canvas[py, px] = self.color if ix < fill_w else self.bg
