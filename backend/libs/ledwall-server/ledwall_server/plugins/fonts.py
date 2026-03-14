"""Shared font loading and crisp text rendering for LED displays.

All text rendering uses 1-bit mode (no anti-aliasing) since LED pixels
are either on or off — gray intermediate values look muddy.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def load_font(size: int = 8) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Load a monospace font at the given pixel size."""
    try:
        return ImageFont.truetype(_FONT_PATH, size)
    except OSError:
        return ImageFont.load_default(size=size)


def render_text(
    text: str,
    width: int,
    height: int,
    color: tuple[int, int, int],
    x: int = 0,
    font_size: int = 8,
) -> np.ndarray:
    """Render text as a crisp (H, W, 3) uint8 array with no anti-aliasing.

    Text is vertically aligned to the top, compensating for the font's
    built-in top padding.
    """
    font = load_font(font_size)
    bbox = font.getbbox(text)
    y_offset = -bbox[1]

    mask = Image.new("1", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.text((x, y_offset), text, fill=1, font=font)

    frame = np.zeros((height, width, 3), dtype=np.uint8)
    frame[np.array(mask)] = color
    return frame


def measure_text(text: str, font_size: int = 8) -> tuple[int, int]:
    """Return (width, height) of rendered text in pixels."""
    font = load_font(font_size)
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]
