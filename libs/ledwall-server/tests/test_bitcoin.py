"""Tests for Bitcoin plugin."""

import json
from unittest.mock import MagicMock, patch

import numpy as np

from ledwall_server.plugins.bitcoin import Bitcoin


def test_bitcoin_creates_five_screens():
    """Bitcoin plugin should create price + 4 trend screens."""
    plugin = Bitcoin({}, 32, 8)
    assert plugin.screen_manager is not None
    assert len(plugin.screen_manager.screens) == 5
    names = [s.name for s in plugin.screen_manager.screens]
    assert names == ["price", "24h", "48h", "7d", "1m"]


def test_bitcoin_renders_without_fetch():
    """Bitcoin should render default data before any fetch."""
    plugin = Bitcoin({}, 32, 8)
    frame = plugin.render()
    assert frame.shape == (8, 32, 3)
    assert frame.dtype == np.uint8


def test_bitcoin_tick_triggers_fetch():
    """First tick should trigger a bitcoin fetch."""
    plugin = Bitcoin({}, 32, 8)
    with patch.object(plugin, "_fetch_bitcoin") as mock_fetch:
        plugin.tick()
        mock_fetch.assert_called_once()


def test_bitcoin_fetch_updates_data():
    """Mock fetch should update price and trend percentages."""
    plugin = Bitcoin({}, 32, 8)

    # Build 31 daily data points (index 0..30)
    # Price goes from 80000 to 100000 linearly for simplicity
    prices = [[1700000000 + i * 86400, 80000 + i * (20000 / 30)] for i in range(31)]
    # Override specific points for deterministic trend assertions
    prices[-1][1] = 100000.0  # current (last)
    prices[-2][1] = 97000.0  # 24h ago
    prices[-3][1] = 101000.0  # 48h ago
    prices[-8][1] = 90000.0  # 7d ago
    prices[0][1] = 80000.0  # 30d ago

    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"prices": prices}).encode()
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_response):
        plugin._fetch_bitcoin()

    assert plugin._price == 100000.0
    assert plugin._fetched is True
    # 24h: (100000 - 97000) / 97000 * 100 ≈ 3.09%
    assert abs(plugin._trends["24h"] - 3.09) < 0.1
    # 48h: (100000 - 101000) / 101000 * 100 ≈ -0.99%
    assert abs(plugin._trends["48h"] - (-0.99)) < 0.1
    # 7d: (100000 - 90000) / 90000 * 100 ≈ 11.11%
    assert abs(plugin._trends["7d"] - 11.11) < 0.1
    # 30d: (100000 - 80000) / 80000 * 100 = 25.0%
    assert abs(plugin._trends["1m"] - 25.0) < 0.1


def test_format_price_large():
    """Prices >= 1000 should use k suffix."""
    plugin = Bitcoin({}, 32, 8)
    assert plugin._format_price(97200.0) == "$97.2k"
    assert plugin._format_price(100000.0) == "$100.0k"
    assert plugin._format_price(1000.0) == "$1.0k"


def test_format_price_small():
    """Prices < 1000 should show as integer dollars."""
    plugin = Bitcoin({}, 32, 8)
    assert plugin._format_price(950.0) == "$950"
    assert plugin._format_price(42.5) == "$42"


def test_trend_positive_uses_green_and_arrow_up():
    """Positive trend should use green color and arrow_up icon."""
    plugin = Bitcoin({}, 32, 8)
    plugin._price = 100000.0
    plugin._trends = {"24h": 2.3, "48h": 1.5, "7d": 5.2, "1m": 12.1}
    plugin._fetched = True
    plugin.screen_manager.screens = plugin._build_screens()

    # Check 24h screen (index 1)
    screen_24h = plugin.screen_manager.screens[1]
    icon_el = screen_24h.elements[0]
    text_el = screen_24h.elements[1]
    assert icon_el.icon == "arrow_up"
    assert icon_el.color == (0, 255, 0)
    assert text_el.color == (0, 255, 0)


def test_trend_negative_uses_red_and_arrow_down():
    """Negative trend should use red color and arrow_down icon."""
    plugin = Bitcoin({}, 32, 8)
    plugin._price = 100000.0
    plugin._trends = {"24h": -1.5, "48h": -3.0, "7d": -0.5, "1m": -10.0}
    plugin._fetched = True
    plugin.screen_manager.screens = plugin._build_screens()

    # Check 24h screen (index 1)
    screen_24h = plugin.screen_manager.screens[1]
    icon_el = screen_24h.elements[0]
    text_el = screen_24h.elements[1]
    assert icon_el.icon == "arrow_down"
    assert icon_el.color == (255, 0, 0)
    assert text_el.color == (255, 0, 0)


def test_bitcoin_fetch_failure_keeps_data():
    """Failed fetch should keep showing last known data."""
    plugin = Bitcoin({}, 32, 8)
    plugin._price = 95000.0
    plugin._trends = {"24h": 1.0, "48h": 2.0, "7d": 3.0, "1m": 4.0}
    plugin._fetched = True

    with patch("urllib.request.urlopen", side_effect=Exception("network error")):
        plugin._fetch_bitcoin()

    assert plugin._price == 95000.0
    assert plugin._trends["24h"] == 1.0


def test_bitcoin_screens_rebuild_after_fetch():
    """Screens should reflect updated data after fetch."""
    plugin = Bitcoin({}, 32, 8)

    prices = [[1700000000 + i * 86400, 90000 + i * 100] for i in range(31)]
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps({"prices": prices}).encode()
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_response):
        plugin._fetch_bitcoin()

    # Price screen should contain formatted price
    price_screen = plugin.screen_manager.screens[0]
    text_el = price_screen.elements[1]
    assert "$" in text_el.text
    assert "k" in text_el.text
