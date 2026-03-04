"""Tests for Weather plugin."""

import json
from unittest.mock import MagicMock, patch

import numpy as np

from ledwall_server.plugins.weather import Weather


def test_weather_creates_screens():
    """Weather plugin should create temp and humidity screens."""
    plugin = Weather({"lat": 45.46, "lon": 9.19}, 16, 8)
    assert plugin.screen_manager is not None
    assert len(plugin.screen_manager.screens) == 2
    assert plugin.screen_manager.screens[0].name == "temp"
    assert plugin.screen_manager.screens[1].name == "humidity"


def test_weather_renders_without_fetch():
    """Weather should render default data before any fetch."""
    plugin = Weather({}, 16, 8)
    frame = plugin.render()
    assert frame.shape == (8, 16, 3)
    assert frame.dtype == np.uint8


def test_weather_tick_triggers_fetch():
    """First tick should trigger a weather fetch."""
    plugin = Weather({}, 16, 8)
    with patch.object(plugin, "_fetch_weather") as mock_fetch:
        plugin.tick()
        mock_fetch.assert_called_once()


def test_weather_fetch_updates_data():
    """Mock fetch should update temperature and humidity."""
    plugin = Weather({"lat": 45.46, "lon": 9.19}, 16, 8)
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps(
        {
            "current": {
                "temperature_2m": 22.5,
                "relative_humidity_2m": 65.0,
                "weather_code": 0,
            }
        }
    ).encode()
    mock_response.__enter__ = lambda s: s
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("urllib.request.urlopen", return_value=mock_response):
        plugin._fetch_weather()

    assert plugin._temp == "22"
    assert plugin._humidity == "65"
    assert plugin._weather_code == 0
    assert plugin._fetched is True


def test_weather_icon_mapping():
    """Weather icon should map WMO codes correctly."""
    plugin = Weather({}, 16, 8)
    plugin._weather_code = 0
    assert plugin._weather_icon == "sun"
    plugin._weather_code = 2
    assert plugin._weather_icon == "cloud_sun"
    plugin._weather_code = 45
    assert plugin._weather_icon == "cloud"
    plugin._weather_code = 61
    assert plugin._weather_icon == "rain"
    plugin._weather_code = 73
    assert plugin._weather_icon == "snow"
    plugin._weather_code = 95
    assert plugin._weather_icon == "storm"


def test_weather_fetch_failure_keeps_data():
    """Failed fetch should keep showing last known data."""
    plugin = Weather({}, 16, 8)
    plugin._temp = "20"
    plugin._humidity = "50"
    plugin._fetched = True

    with patch("urllib.request.urlopen", side_effect=Exception("network error")):
        plugin._fetch_weather()

    assert plugin._temp == "20"
    assert plugin._humidity == "50"
