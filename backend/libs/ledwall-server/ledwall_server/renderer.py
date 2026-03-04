"""Frame compositor — composites plugin outputs into a final frame."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ledwall_server.plugins.base import BasePlugin


class Renderer:
    """Composes plugin layers into a single (height, width, 3) RGB frame."""

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def compose(self, layers: list[tuple[BasePlugin, int, int]]) -> np.ndarray:
        """Compose plugin outputs at (x, y) positions into final frame.

        Args:
            layers: list of (plugin, x_offset, y_offset) tuples

        Returns:
            (height, width, 3) uint8 RGB numpy array
        """
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        for plugin, x, y in layers:
            overlay = plugin.render()
            oh, ow = overlay.shape[:2]
            # Compute clipped region
            src_y0 = max(0, -y)
            src_x0 = max(0, -x)
            dst_y0 = max(0, y)
            dst_x0 = max(0, x)
            h = min(oh - src_y0, self.height - dst_y0)
            w = min(ow - src_x0, self.width - dst_x0)
            if h <= 0 or w <= 0:
                continue
            # Non-zero pixels overwrite (simple compositing)
            src = overlay[src_y0 : src_y0 + h, src_x0 : src_x0 + w]
            mask = np.any(src > 0, axis=2)
            dst = frame[dst_y0 : dst_y0 + h, dst_x0 : dst_x0 + w]
            dst[mask] = src[mask]
        return frame
