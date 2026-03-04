"""Fallback display mode when server is unreachable."""

import uasyncio as asyncio

from picow_ws2812.fonts import BASEFONT


class FallbackMode:
    """Simple display when server is unreachable.

    Shows scrolling IP address and a basic color cycle.
    Auto-switches back when server packets resume.
    """

    def __init__(self, timeout=5):
        """Initialize fallback mode.

        Args:
            timeout: seconds without packets before activating fallback
        """
        self.timeout = timeout
        self._active = False

    @property
    def is_active(self):
        """Return True if fallback mode is currently active."""
        return self._active

    async def watch(self, receiver, ledwall, wifi_manager=None):
        """Monitor receiver and activate fallback when no packets arrive.

        Args:
            receiver: FrameReceiver instance
            ledwall: LedWall instance
            wifi_manager: optional WiFiManager for IP display
        """
        while True:
            if receiver.seconds_since_last_packet > self.timeout:
                if not self._active:
                    self._active = True
                    print("Fallback mode activated")
                await self._run_fallback(ledwall, wifi_manager)
            else:
                if self._active:
                    self._active = False
                    print("Server resumed, exiting fallback")
            await asyncio.sleep(1)

    async def _run_fallback(self, ledwall, wifi_manager):
        """Run one frame of fallback display."""
        if wifi_manager and wifi_manager.ip_address:
            self._show_text(ledwall, wifi_manager.ip_address)
        else:
            self._color_cycle(ledwall)

    def _show_text(self, ledwall, text, color=(0, 40, 0)):
        """Render text string to LED wall using bitmap font.

        Renders at position (0, 0), clipping to wall dimensions.
        """
        ledwall.clear()
        x_cursor = 0
        for ch in text.upper():
            if ch in BASEFONT:
                glyph = BASEFONT[ch]
                for dy, row in enumerate(glyph):
                    for dx, pixel in enumerate(row):
                        if pixel == "1":
                            px = x_cursor + dx
                            py = dy
                            if 0 <= px < ledwall.ncols and 0 <= py < ledwall.nrows:
                                ledwall.set_pixel_xy(px, py, color)
                x_cursor += 6  # 5 wide + 1 gap
        ledwall.show()

    def _color_cycle(self, ledwall):
        """Simple color fill as a heartbeat indicator."""
        ledwall.fill((0, 0, 20))
        ledwall.show()
