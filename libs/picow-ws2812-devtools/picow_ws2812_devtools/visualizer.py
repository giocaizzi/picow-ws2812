"""LED wall visualizer — preview plugins and scenes in matplotlib.

Works in Jupyter notebooks with `%matplotlib ipympl`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

if TYPE_CHECKING:
    from ledwall_server.plugins.base import BasePlugin
    from ledwall_server.renderer import Renderer


class LedWallVisualizer:
    """Preview LED wall plugins and composed scenes.

    Usage in notebook::

        %matplotlib ipympl

        from ledwall_server.plugins.effect import Rainbow
        from picow_ws2812_devtools.visualizer import LedWallVisualizer

        viz = LedWallVisualizer()
        viz.preview_plugin(Rainbow({"speed": 3}, 32, 24))
    """

    def __init__(self, width: int = 32, height: int = 24):
        self.width = width
        self.height = height
        self._ani: FuncAnimation | None = None

    def preview_plugin(
        self,
        plugin: BasePlugin,
        frames: int = 100,
        interval: int = 33,
    ) -> None:
        """Animate a single plugin."""
        fig, ax = plt.subplots()
        ax.set_title(type(plugin).__name__)
        im = ax.imshow(
            np.zeros((plugin.height, plugin.width, 3), dtype=np.uint8),
            interpolation="nearest",
        )
        ax.axis("off")

        def update(_frame_num: int):
            plugin.tick()
            im.set_data(plugin.render())
            return (im,)

        self._ani = FuncAnimation(fig, update, frames=frames, interval=interval)
        plt.show()

    def preview_scene(
        self,
        renderer: Renderer,
        layers: list[tuple[BasePlugin, int, int]],
        frames: int = 100,
        interval: int = 33,
    ) -> None:
        """Animate a composed scene using Renderer."""
        fig, ax = plt.subplots()
        ax.set_title("Scene Preview")
        im = ax.imshow(
            np.zeros((self.height, self.width, 3), dtype=np.uint8),
            interpolation="nearest",
        )
        ax.axis("off")

        def update(_frame_num: int):
            for plugin, _, _ in layers:
                plugin.tick()
            frame = renderer.compose(layers)
            im.set_data(frame)
            return (im,)

        self._ani = FuncAnimation(fig, update, frames=frames, interval=interval)
        plt.show()

    def snapshot(
        self,
        plugin: BasePlugin | None = None,
        renderer: Renderer | None = None,
        layers: list[tuple[BasePlugin, int, int]] | None = None,
    ) -> None:
        """Show a single frame (no animation)."""
        if renderer is not None and layers is not None:
            for p, _, _ in layers:
                p.tick()
            frame = renderer.compose(layers)
        elif plugin is not None:
            plugin.tick()
            frame = plugin.render()
        else:
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        fig, ax = plt.subplots()
        ax.imshow(frame, interpolation="nearest")
        ax.axis("off")
        plt.show()
