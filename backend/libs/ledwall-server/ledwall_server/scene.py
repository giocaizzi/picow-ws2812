"""Scene manager — manages active scene and render loop."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ledwall_server.plugins.base import BasePlugin
    from ledwall_server.renderer import Renderer
    from ledwall_server.sender import FrameSender


class SceneManager:
    """Manages the active scene and runs the render loop.

    A scene is a list of (plugin, x_offset, y_offset) tuples
    that get composed together each frame.
    """

    def __init__(self, renderer: Renderer, sender: FrameSender, fps: int = 30):
        self.renderer = renderer
        self.sender = sender
        self.fps = fps
        self.active_scene: list[tuple[BasePlugin, int, int]] = []
        self._seq = 0
        self._running = False

    def set_scene(self, layers: list[tuple[BasePlugin, int, int]]) -> None:
        """Replace the active scene."""
        self.active_scene = layers

    async def run(self) -> None:
        """Main render loop: tick plugins → compose → send."""
        self._running = True
        interval = 1.0 / self.fps
        while self._running:
            if self.active_scene:
                for plugin, _, _ in self.active_scene:
                    plugin.tick()
                frame = self.renderer.compose(self.active_scene)
                self.sender.send_frame(frame, self._seq)
                self._seq = (self._seq + 1) % 16
            await asyncio.sleep(interval)

    def stop(self) -> None:
        """Stop the render loop."""
        self._running = False
