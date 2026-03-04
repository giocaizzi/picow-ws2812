"""Clock widget plugin — displays current time using elements/screens."""

from datetime import datetime

from ledwall_server.plugins.base import BasePlugin
from ledwall_server.plugins.elements import TextElement
from ledwall_server.plugins.screen import Screen, ScreenManager


class Clock(BasePlugin):
    """Display the current time as HH:MM."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self.color = tuple(config.get("color", [255, 255, 255]))
        self._time_str = datetime.now().strftime("%H:%M")

        self._text_element = TextElement(
            0, 0, width, height, text=self._time_str, color=self.color
        )
        self.screen_manager = ScreenManager(
            screens=[Screen("time", [self._text_element])],
            mode="fixed",
        )

    def tick(self) -> None:
        self._time_str = datetime.now().strftime("%H:%M")
        self._text_element.text = self._time_str
