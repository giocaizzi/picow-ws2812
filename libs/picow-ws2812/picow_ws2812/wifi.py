"""WiFi connection manager for Pico W."""

import network
import uasyncio as asyncio


class WiFiManager:
    """Manages WiFi connection with auto-reconnect."""

    def __init__(self):
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        self._ip = ""
        self._ssid = ""
        self._password = ""

    @property
    def is_connected(self):
        """Return True if WiFi is connected."""
        return self._wlan.isconnected()

    @property
    def ip_address(self):
        """Return current IP address string."""
        if self.is_connected:
            self._ip = self._wlan.ifconfig()[0]
        return self._ip

    async def connect(self, ssid, password, max_retries=10):
        """Connect to WiFi network.

        Args:
            ssid: network SSID
            password: network password
            max_retries: max connection attempts before giving up
        """
        self._ssid = ssid
        self._password = password
        self._wlan.connect(ssid, password)
        for _ in range(max_retries):
            if self.is_connected:
                self._ip = self._wlan.ifconfig()[0]
                print("WiFi connected:", self._ip)
                return True
            await asyncio.sleep(1)
        print("WiFi connection failed after", max_retries, "retries")
        return False

    async def monitor(self, check_interval=5):
        """Continuously monitor WiFi and reconnect if dropped.

        This coroutine runs forever. Call it via asyncio.gather().

        Args:
            check_interval: seconds between connection checks
        """
        while True:
            if not self.is_connected:
                print("WiFi disconnected, attempting reconnect...")
                self._wlan.connect(self._ssid, self._password)
                for _ in range(10):
                    if self.is_connected:
                        self._ip = self._wlan.ifconfig()[0]
                        print("WiFi reconnected:", self._ip)
                        break
                    await asyncio.sleep(2)
            await asyncio.sleep(check_interval)
