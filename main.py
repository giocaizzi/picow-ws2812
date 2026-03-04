"""Pico W LED wall entry point — connects to WiFi and receives frames via UDP."""

import uasyncio as asyncio

from picow_ws2812.fallback import FallbackMode
from picow_ws2812.ledwall import LedWall
from picow_ws2812.protocol import DEFAULT_PORT
from picow_ws2812.receiver import FrameReceiver
from picow_ws2812.wifi import WiFiManager

# --- Configuration ---
SSID = "YOUR_SSID"
PASSWORD = "YOUR_PASSWORD"
GPIO_PIN = 28

STRIPS_CONFIG = [
    {"nrows": 8, "ncols": 32, "y_offset": 0, "zigzag": True},
    {"nrows": 8, "ncols": 32, "y_offset": 8, "zigzag": True},
    {"nrows": 8, "ncols": 32, "y_offset": 16, "zigzag": True},
]


async def main():
    wifi = WiFiManager()
    connected = await wifi.connect(SSID, PASSWORD)
    if not connected:
        print("Could not connect to WiFi, running in offline mode")

    ledwall = LedWall(STRIPS_CONFIG, GPIO_PIN)
    receiver = FrameReceiver(ledwall, port=DEFAULT_PORT)
    fallback = FallbackMode(timeout=5)

    print("Starting LED wall receiver...")
    await asyncio.gather(
        wifi.monitor(),
        receiver.listen(),
        fallback.watch(receiver, ledwall, wifi),
    )


asyncio.run(main())
