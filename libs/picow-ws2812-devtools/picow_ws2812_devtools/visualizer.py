"""LED wall visualizer — preview plugins and scenes in matplotlib.

Works in Jupyter notebooks with `%matplotlib ipympl`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle

if TYPE_CHECKING:
    from ledwall_server.plugins.base import BasePlugin
    from ledwall_server.renderer import Renderer


class LedWallVisualizer:
    """Preview LED wall plugins and composed scenes.

    Each LED is rendered as a circle on a dark background,
    simulating the look of a real LED panel.

    Usage in notebook::

        %matplotlib ipympl

        from ledwall_server.plugins.effect import Rainbow
        from picow_ws2812_devtools.visualizer import LedWallVisualizer

        viz = LedWallVisualizer()
        viz.preview_plugin(Rainbow({"speed": 3}, 32, 24))

    Args:
        width: Number of horizontal LEDs.
        height: Number of vertical LEDs.
        dot_radius: Radius of each LED dot in cell units.
            Each cell is 1×1, so max radius is 0.5.
    """

    def __init__(
        self,
        width: int = 32,
        height: int = 24,
        dot_radius: float = 0.4,
    ):
        if dot_radius <= 0 or dot_radius > 0.5:
            raise ValueError("dot_radius must be in (0, 0.5]")
        self.width = width
        self.height = height
        self.dot_radius = dot_radius
        self._ani: FuncAnimation | None = None

    def _create_led_plot(
        self,
        width: int,
        height: int,
        title: str,
    ) -> tuple[plt.Figure, plt.Axes, PatchCollection]:
        """Set up figure with circular LED patches on a dark background."""
        fig, ax = plt.subplots()
        ax.set_title(title, color="white")
        ax.set_facecolor("black")
        fig.set_facecolor("black")
        ax.set_xlim(0, width)
        ax.set_ylim(height, 0)
        ax.set_aspect("equal")
        ax.axis("off")

        patches = [
            Circle((col + 0.5, row + 0.5), self.dot_radius)
            for row in range(height)
            for col in range(width)
        ]
        collection = PatchCollection(patches, match_original=False)
        collection.set_edgecolor("none")
        collection.set_facecolor(np.zeros((height * width, 3)))
        ax.add_collection(collection)

        return fig, ax, collection

    @staticmethod
    def _frame_to_colors(frame: np.ndarray) -> np.ndarray:
        """Convert (H, W, 3) uint8 frame to (H*W, 4) RGBA float colors."""
        rgb = frame.reshape(-1, 3).astype(np.float64) / 255.0
        alpha = np.ones((rgb.shape[0], 1))
        return np.hstack([rgb, alpha])

    def render_frame(self, ax: plt.Axes, frame: np.ndarray) -> PatchCollection:
        """Render a (H, W, 3) uint8 frame as LED dots on an existing axes."""
        height, width = frame.shape[:2]
        ax.set_facecolor("black")
        ax.set_xlim(0, width)
        ax.set_ylim(height, 0)
        ax.set_aspect("equal")
        ax.axis("off")

        patches = [
            Circle((col + 0.5, row + 0.5), self.dot_radius)
            for row in range(height)
            for col in range(width)
        ]
        collection = PatchCollection(patches, match_original=False)
        collection.set_edgecolor("none")
        collection.set_facecolor(self._frame_to_colors(frame))
        ax.add_collection(collection)
        return collection

    def preview_plugin(
        self,
        plugin: BasePlugin,
        frames: int = 100,
        interval: int = 33,
    ) -> None:
        """Animate a single plugin."""
        _, _, collection = self._create_led_plot(
            plugin.width, plugin.height, type(plugin).__name__
        )

        def update(_frame_num: int):
            plugin.tick()
            collection.set_facecolor(self._frame_to_colors(plugin.render()))
            return (collection,)

        self._ani = FuncAnimation(
            collection.axes.figure, update, frames=frames, interval=interval
        )
        plt.show()

    def preview_scene(
        self,
        renderer: Renderer,
        layers: list[tuple[BasePlugin, int, int]],
        frames: int = 100,
        interval: int = 33,
    ) -> None:
        """Animate a composed scene using Renderer."""
        _, _, collection = self._create_led_plot(
            self.width, self.height, "Scene Preview"
        )

        def update(_frame_num: int):
            for plugin, _, _ in layers:
                plugin.tick()
            frame = renderer.compose(layers)
            collection.set_facecolor(self._frame_to_colors(frame))
            return (collection,)

        self._ani = FuncAnimation(
            collection.axes.figure, update, frames=frames, interval=interval
        )
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
            width, height = self.width, self.height
        elif plugin is not None:
            plugin.tick()
            frame = plugin.render()
            width, height = plugin.width, plugin.height
        else:
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            width, height = self.width, self.height

        _, _, collection = self._create_led_plot(width, height, "Snapshot")
        collection.set_facecolor(self._frame_to_colors(frame))
        plt.show()
