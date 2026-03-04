"""Weather plugin — displays live weather data from Open-Meteo API.

Uses elements and screens for composable multi-view display.
"""

from __future__ import annotations

import json
import logging
import urllib.request

from ledwall_server.plugins.base import BasePlugin
from ledwall_server.plugins.elements import IconElement, TextElement
from ledwall_server.plugins.screen import Screen, ScreenManager

logger = logging.getLogger(__name__)


class Weather(BasePlugin):
    """Display weather information from Open-Meteo (free, no API key)."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self._lat = config.get("lat", 45.46)
        self._lon = config.get("lon", 9.19)
        self._fetch_interval = config.get("fetch_interval", 600)
        self._temp = "--"
        self._weather_code = 0
        self._humidity = "--"
        self._tick_count = 0
        self._fetched = False

        self.screen_manager = ScreenManager(
            screens=self._build_screens(),
            mode=config.get("screen_mode", "auto"),
            interval=config.get("screen_interval", 90),
        )

    def _build_screens(self) -> list[Screen]:
        return [
            Screen(
                "temp",
                [
                    IconElement(
                        0, 0, 8, 8, icon=self._weather_icon, color=(255, 200, 0)
                    ),
                    TextElement(
                        9,
                        1,
                        self.width - 9,
                        7,
                        text=f"{self._temp}\u00b0",
                        color=(255, 255, 255),
                    ),
                ],
            ),
            Screen(
                "humidity",
                [
                    IconElement(0, 0, 8, 8, icon="drop", color=(0, 150, 255)),
                    TextElement(
                        9,
                        1,
                        self.width - 9,
                        7,
                        text=f"{self._humidity}%",
                        color=(255, 255, 255),
                    ),
                ],
            ),
        ]

    def tick(self) -> None:
        self._tick_count += 1
        if not self._fetched or self._tick_count % (self._fetch_interval * 30) == 0:
            self._fetch_weather()
        self.screen_manager.tick()

    def _fetch_weather(self) -> None:
        """Fetch current weather from Open-Meteo."""
        try:
            url = (
                f"https://api.open-meteo.com/v1/forecast"
                f"?latitude={self._lat}&longitude={self._lon}"
                f"&current=temperature_2m,relative_humidity_2m,weather_code"
            )
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read())
            current = data["current"]
            self._temp = str(int(current["temperature_2m"]))
            self._humidity = str(int(current["relative_humidity_2m"]))
            self._weather_code = current["weather_code"]
            self._fetched = True
            self.screen_manager.screens = self._build_screens()
        except Exception:
            logger.exception("Failed to fetch weather data")

    @property
    def _weather_icon(self) -> str:
        """Map WMO weather code to icon name."""
        code = self._weather_code
        if code == 0:
            return "sun"
        if code in (1, 2, 3):
            return "cloud_sun"
        if code in (45, 48):
            return "cloud"
        if code in range(51, 68):
            return "rain"
        if code in range(71, 78):
            return "snow"
        if code in range(80, 83):
            return "rain"
        if code in range(95, 100):
            return "storm"
        return "cloud"
