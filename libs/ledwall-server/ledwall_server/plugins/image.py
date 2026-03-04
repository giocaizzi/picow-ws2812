"""Image plugin — display a static image or GIF."""

import numpy as np
from PIL import Image

from ledwall_server.plugins.base import BasePlugin


class StaticImage(BasePlugin):
    """Display a static image scaled to the display size."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        path = config.get("path", "")
        if path:
            img = Image.open(path).convert("RGB").resize((width, height), Image.NEAREST)
            self._frame = np.array(img, dtype=np.uint8)
        else:
            self._frame = np.zeros((height, width, 3), dtype=np.uint8)

    def render(self) -> np.ndarray:
        return self._frame

    def tick(self) -> None:
        pass


class AnimatedGif(BasePlugin):
    """Display an animated GIF, cycling through frames."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        path = config.get("path", "")
        self._frames: list[np.ndarray] = []
        self._current = 0
        if path:
            img = Image.open(path)
            try:
                while True:
                    frame = img.convert("RGB").resize((width, height), Image.NEAREST)
                    self._frames.append(np.array(frame, dtype=np.uint8))
                    img.seek(img.tell() + 1)
            except EOFError:
                pass
        if not self._frames:
            self._frames.append(np.zeros((height, width, 3), dtype=np.uint8))

    def render(self) -> np.ndarray:
        return self._frames[self._current]

    def tick(self) -> None:
        self._current = (self._current + 1) % len(self._frames)
