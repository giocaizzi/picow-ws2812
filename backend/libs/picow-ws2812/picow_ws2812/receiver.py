"""UDP frame receiver for Pico W — receives pixel data from Pi5 server."""

import socket
import time

import uasyncio as asyncio

from picow_ws2812.protocol import (
    CFG_BRIGHTNESS,
    CFG_DIMENSIONS,
    CMD_CLEAR,
    CMD_CONFIG,
    CMD_FRAME_DATA,
    CMD_PING,
    CMD_PONG,
    DEFAULT_PORT,
    FLAG_PUSH,
    HEADER_SIZE,
    STATUS_IDLE,
    STATUS_RECEIVING,
    build_header,
    parse_header,
)


class FrameReceiver:
    """Receives UDP frames and writes them to the LedWall."""

    def __init__(self, ledwall, port=DEFAULT_PORT):
        """Initialize receiver.

        Args:
            ledwall: LedWall instance
            port: UDP port to listen on
        """
        self.ledwall = ledwall
        self.port = port
        self.num_leds = ledwall.num_leds
        self._buf = bytearray(self.num_leds * 3)
        self._last_packet_time = 0
        self._status = STATUS_IDLE
        self._sock = None

    @property
    def last_packet_time(self):
        """Time of last received packet (time.ticks_ms)."""
        return self._last_packet_time

    @property
    def seconds_since_last_packet(self):
        """Seconds elapsed since last packet."""
        if self._last_packet_time == 0:
            return 999
        return time.ticks_diff(time.ticks_ms(), self._last_packet_time) / 1000

    async def listen(self):
        """Main receive loop. Non-blocking UDP recv via polling."""
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(("0.0.0.0", self.port))
        self._sock.setblocking(False)
        print("UDP receiver listening on port", self.port)

        while True:
            try:
                data, addr = self._sock.recvfrom(1500)
                self._last_packet_time = time.ticks_ms()
                self._dispatch(data, addr)
            except OSError:
                # EAGAIN — no data available
                pass
            await asyncio.sleep_ms(1)

    def _dispatch(self, data, addr):
        """Parse header and dispatch to handler."""
        parsed = parse_header(data)
        if parsed is None:
            return

        command, flags, sequence, offset, length = parsed
        payload = data[HEADER_SIZE:]

        if command == CMD_FRAME_DATA:
            self._status = STATUS_RECEIVING
            self._handle_frame_data(payload, offset, length, flags)
        elif command == CMD_PING:
            self._handle_ping(addr)
        elif command == CMD_CONFIG:
            self._handle_config(payload)
        elif command == CMD_CLEAR:
            self.ledwall.clear()
            self.ledwall.show()
            self._status = STATUS_IDLE

    def _handle_frame_data(self, payload, offset, length, flags):
        """Write RGB bytes into frame buffer at pixel offset.

        On PUSH flag: apply buffer to neopixels and show().
        """
        byte_offset = offset * 3
        byte_length = length * 3
        # Bounds-check and copy payload into buffer
        end = min(byte_offset + byte_length, len(self._buf))
        available = min(len(payload), end - byte_offset)
        self._buf[byte_offset : byte_offset + available] = payload[:available]

        if flags & FLAG_PUSH:
            self._apply_frame()
            self._status = STATUS_IDLE

    def _apply_frame(self):
        """Transfer frame buffer to neopixel pixel array and show().

        Writes directly to the neopixel.pixels array for performance.
        """
        pixels = self.ledwall.pixels
        shift = self.ledwall.shift
        sh_R, sh_G, sh_B = shift[0], shift[1], shift[2]
        brightness = self.ledwall.brightness()
        bratio = brightness / 255.0
        buf = self._buf

        for i in range(self.num_leds):
            base = i * 3
            r = int(buf[base] * bratio)
            g = int(buf[base + 1] * bratio)
            b = int(buf[base + 2] * bratio)
            pixels[i] = (b << sh_B) | (r << sh_R) | (g << sh_G)

        self.ledwall.show()

    def _handle_ping(self, addr):
        """Respond to PING with PONG containing device info."""
        header = build_header(CMD_PONG, 0, 0, 0, 0)
        nrows = self.ledwall.nrows
        ncols = self.ledwall.ncols
        brightness = self.ledwall.brightness()
        payload = bytes(
            [
                (nrows >> 8) & 0xFF,
                nrows & 0xFF,
                (ncols >> 8) & 0xFF,
                ncols & 0xFF,
                brightness,
                self._status,
            ]
        )
        self._sock.sendto(header + payload, addr)

    def _handle_config(self, payload):
        """Handle CONFIG commands."""
        if len(payload) < 1:
            return
        key = payload[0]
        if key == CFG_BRIGHTNESS and len(payload) >= 2:
            self.ledwall.brightness(payload[1])
        elif key == CFG_DIMENSIONS and len(payload) >= 3:
            # Read-only for now; dimensions are set at init
            pass
