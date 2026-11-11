"""Protocol constants for Pi5 ↔ Pico W UDP communication.

Mirror of picow_ws2812.protocol for the server side.
"""

# Command types
CMD_FRAME_DATA = 0x01
CMD_CONFIG = 0x02
CMD_PING = 0x03
CMD_PONG = 0x04
CMD_CLEAR = 0x05

# Flags (byte 1, bits 7-4)
FLAG_PUSH = 0x80

# Config keys
CFG_BRIGHTNESS = 0x01
CFG_DIMENSIONS = 0x02

# Status codes (PONG response)
STATUS_IDLE = 0x00
STATUS_RECEIVING = 0x01
STATUS_FALLBACK = 0x02

# Network
DEFAULT_PORT = 21324

# Protocol header size in bytes
HEADER_SIZE = 6

# Max pixels per UDP packet (limited by ~1472 byte MTU)
MAX_PIXELS_PER_PACKET = 480


def parse_header(data: bytes) -> tuple | None:
    """Parse a 6-byte protocol header.

    Returns (command, flags, sequence, offset, length) or None if invalid.
    """
    if len(data) < HEADER_SIZE:
        return None
    command = data[0]
    flags = data[1] & 0xF0
    sequence = data[1] & 0x0F
    offset = (data[2] << 8) | data[3]
    length = (data[4] << 8) | data[5]
    return command, flags, sequence, offset, length


def build_header(
    command: int, flags: int, sequence: int, offset: int, length: int
) -> bytes:
    """Build a 6-byte protocol header."""
    return bytes(
        [
            command,
            (flags & 0xF0) | (sequence & 0x0F),
            (offset >> 8) & 0xFF,
            offset & 0xFF,
            (length >> 8) & 0xFF,
            length & 0xFF,
        ]
    )
