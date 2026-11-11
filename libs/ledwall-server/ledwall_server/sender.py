"""UDP frame sender — packetizes numpy frames and sends to Pico W."""

import socket

import numpy as np

from ledwall_server.protocol import (
    CFG_BRIGHTNESS,
    CMD_CLEAR,
    CMD_CONFIG,
    CMD_FRAME_DATA,
    CMD_PING,
    FLAG_PUSH,
    HEADER_SIZE,
    MAX_PIXELS_PER_PACKET,
    build_header,
    parse_header,
)


class FrameSender:
    """Sends rendered frames to a Pico W over UDP."""

    def __init__(self, target_ip: str, port: int = 21324):
        self.target = (target_ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(2.0)

    def send_frame(self, frame: np.ndarray, seq: int) -> None:
        """Packetize a (H, W, 3) uint8 RGB frame and send via UDP.

        Splits into chunks of MAX_PIXELS_PER_PACKET pixels.
        Sets PUSH flag on the last packet.
        """
        flat = frame.reshape(-1, 3).astype(np.uint8)
        total_pixels = flat.shape[0]
        offset = 0

        while offset < total_pixels:
            chunk_size = min(MAX_PIXELS_PER_PACKET, total_pixels - offset)
            is_last = (offset + chunk_size) >= total_pixels
            flags = FLAG_PUSH if is_last else 0
            header = build_header(CMD_FRAME_DATA, flags, seq, offset, chunk_size)
            payload = flat[offset : offset + chunk_size].tobytes()
            self.sock.sendto(header + payload, self.target)
            offset += chunk_size

    def send_ping(self) -> dict | None:
        """Send PING and wait for PONG with device info.

        Returns dict with nrows, ncols, brightness, status or None on timeout.
        """
        header = build_header(CMD_PING, 0, 0, 0, 0)
        self.sock.sendto(header, self.target)
        try:
            data, _ = self.sock.recvfrom(64)
            parsed = parse_header(data)
            if parsed is None:
                return None
            payload = data[HEADER_SIZE:]
            if len(payload) < 6:
                return None
            return {
                "nrows": (payload[0] << 8) | payload[1],
                "ncols": (payload[2] << 8) | payload[3],
                "brightness": payload[4],
                "status": payload[5],
            }
        except TimeoutError:
            return None

    def send_clear(self) -> None:
        """Send CLEAR command."""
        header = build_header(CMD_CLEAR, 0, 0, 0, 0)
        self.sock.sendto(header, self.target)

    def send_brightness(self, value: int) -> None:
        """Send CONFIG brightness command."""
        header = build_header(CMD_CONFIG, 0, 0, 0, 0)
        payload = bytes([CFG_BRIGHTNESS, max(1, min(255, value))])
        self.sock.sendto(header + payload, self.target)

    def close(self) -> None:
        """Close the UDP socket."""
        self.sock.close()
