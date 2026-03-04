"""Bitcoin price plugin — displays BTC/USD price and trends from CoinGecko API."""

from __future__ import annotations

import json
import logging
import urllib.request

from ledwall_server.plugins.base import BasePlugin
from ledwall_server.plugins.elements import IconElement, TextElement
from ledwall_server.plugins.screen import Screen, ScreenManager

logger = logging.getLogger(__name__)

_TREND_PERIODS = {
    "24h": -2,
    "48h": -3,
    "7d": -8,
    "1m": 0,
}


class Bitcoin(BasePlugin):
    """Display Bitcoin price and trend data from CoinGecko (free, no API key)."""

    def __init__(self, config: dict, width: int, height: int):
        super().__init__(config, width, height)
        self._vs_currency = config.get("vs_currency", "usd")
        self._fetch_interval = config.get("fetch_interval", 300)
        self._price: float = 0.0
        self._trends: dict[str, float] = {k: 0.0 for k in _TREND_PERIODS}
        self._tick_count = 0
        self._fetched = False

        self.screen_manager = ScreenManager(
            screens=self._build_screens(),
            mode=config.get("screen_mode", "auto"),
            interval=config.get("screen_interval", 90),
        )

    def _build_screens(self) -> list[Screen]:
        price_text = self._format_price(self._price) if self._fetched else "$--"
        screens = [
            Screen(
                "price",
                [
                    IconElement(0, 0, 8, 8, icon="bitcoin", color=(247, 147, 26)),
                    TextElement(
                        9,
                        1,
                        self.width - 9,
                        7,
                        text=price_text,
                        color=(255, 255, 255),
                    ),
                ],
            ),
        ]
        for label in _TREND_PERIODS:
            pct = self._trends[label]
            positive = pct >= 0
            color = (0, 255, 0) if positive else (255, 0, 0)
            icon = "arrow_up" if positive else "arrow_down"
            sign = "+" if positive else ""
            text = f"{label} {sign}{pct:.1f}%" if self._fetched else f"{label} --%"
            screens.append(
                Screen(
                    label,
                    [
                        IconElement(0, 0, 8, 8, icon=icon, color=color),
                        TextElement(
                            9,
                            1,
                            self.width - 9,
                            7,
                            text=text,
                            color=color,
                        ),
                    ],
                ),
            )
        return screens

    def tick(self) -> None:
        self._tick_count += 1
        if not self._fetched or self._tick_count % (self._fetch_interval * 30) == 0:
            self._fetch_bitcoin()
        self.screen_manager.tick()

    def _fetch_bitcoin(self) -> None:
        """Fetch Bitcoin market data from CoinGecko."""
        try:
            url = (
                f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
                f"?vs_currency={self._vs_currency}&days=30&interval=daily"
            )
            with urllib.request.urlopen(url, timeout=10) as resp:
                data = json.loads(resp.read())

            prices = data["prices"]
            current = prices[-1][1]
            self._price = current

            for label, idx in _TREND_PERIODS.items():
                past = prices[idx][1]
                self._trends[label] = round((current - past) / past * 100, 2)

            self._fetched = True
            self.screen_manager.screens = self._build_screens()
        except Exception:
            logger.exception("Failed to fetch Bitcoin data")

    @staticmethod
    def _format_price(price: float) -> str:
        """Format price for LED display."""
        if price >= 1000:
            return f"${price / 1000:.1f}k"
        return f"${int(price)}"
