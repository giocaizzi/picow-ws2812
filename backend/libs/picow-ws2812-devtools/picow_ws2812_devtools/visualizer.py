"""LED wall visualizer — preview plugins and scenes in matplotlib."""

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

    Usage::

        uv run preview Rainbow
        uv run preview Rainbow --gif --frames 60

    Args:
        width: Number of horizontal LEDs.
        height: Number of vertical LEDs.
        dot_radius: Radius of each LED dot in cell units.
            Each cell is 1x1, so max radius is 0.5.
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

    def _render_single_frame(
        self,
        plugin: BasePlugin | None = None,
        renderer: Renderer | None = None,
        layers: list[tuple[BasePlugin, int, int]] | None = None,
    ) -> tuple[np.ndarray, int, int]:
        """Tick once and return (frame, width, height)."""
        if renderer is not None and layers is not None:
            for p, _, _ in layers:
                p.tick()
            return renderer.compose(layers), self.width, self.height
        if plugin is not None:
            plugin.tick()
            return plugin.render(), plugin.width, plugin.height
        return (
            np.zeros((self.height, self.width, 3), dtype=np.uint8),
            self.width,
            self.height,
        )

    def save_snapshot(
        self,
        path: str,
        plugin: BasePlugin | None = None,
        renderer: Renderer | None = None,
        layers: list[tuple[BasePlugin, int, int]] | None = None,
        title: str = "Snapshot",
    ) -> None:
        """Render a single frame and save as PNG."""
        frame, width, height = self._render_single_frame(plugin, renderer, layers)
        fig, _, collection = self._create_led_plot(width, height, title)
        collection.set_facecolor(self._frame_to_colors(frame))
        fig.savefig(path, facecolor="black", bbox_inches="tight", dpi=150)
        plt.close(fig)

    def save_animation(
        self,
        path: str,
        plugin: BasePlugin | None = None,
        renderer: Renderer | None = None,
        layers: list[tuple[BasePlugin, int, int]] | None = None,
        frames: int = 100,
        interval: int = 33,
        title: str = "Animation",
    ) -> None:
        """Render an animation and save as GIF."""
        if plugin is not None:
            width, height = plugin.width, plugin.height
        else:
            width, height = self.width, self.height

        fig, _, collection = self._create_led_plot(width, height, title)

        def update(_frame_num: int):
            if renderer is not None and layers is not None:
                for p, _, _ in layers:
                    p.tick()
                frame = renderer.compose(layers)
            elif plugin is not None:
                plugin.tick()
                frame = plugin.render()
            else:
                frame = np.zeros((height, width, 3), dtype=np.uint8)
            collection.set_facecolor(self._frame_to_colors(frame))
            return (collection,)

        anim = FuncAnimation(fig, update, frames=frames, interval=interval)
        anim.save(path, writer="pillow")
        plt.close(fig)
