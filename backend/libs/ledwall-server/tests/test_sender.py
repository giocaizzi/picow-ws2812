"""Tests for the UDP frame sender."""

from unittest.mock import MagicMock

import numpy as np

from ledwall_server.protocol import (
    FLAG_PUSH,
    HEADER_SIZE,
    MAX_PIXELS_PER_PACKET,
    parse_header,
)
from ledwall_server.sender import FrameSender


def test_send_frame_single_packet():
    """A small frame fits in one packet with PUSH flag."""
    sender = FrameSender("127.0.0.1", 21324)
    sender.sock = MagicMock()

    # 10 pixels = 30 bytes payload, fits in one packet
    frame = np.zeros((1, 10, 3), dtype=np.uint8)
    frame[0, 0] = [255, 0, 0]
    sender.send_frame(frame, seq=0)

    sender.sock.sendto.assert_called_once()
    data, addr = sender.sock.sendto.call_args[0]
    assert addr == ("127.0.0.1", 21324)

    # Parse header
    command, flags, seq, offset, length = parse_header(data[:HEADER_SIZE])
    assert flags == FLAG_PUSH  # single packet = last = PUSH
    assert offset == 0
    assert length == 10
    assert len(data) == HEADER_SIZE + 30  # 10 pixels * 3


def test_send_frame_multiple_packets():
    """A 768-pixel frame splits into 2 packets."""
    sender = FrameSender("127.0.0.1", 21324)
    sender.sock = MagicMock()

    frame = np.zeros((24, 32, 3), dtype=np.uint8)  # 768 pixels
    sender.send_frame(frame, seq=5)

    assert sender.sock.sendto.call_count == 2

    # First packet: no PUSH, offset=0, length=480
    data1 = sender.sock.sendto.call_args_list[0][0][0]
    _, flags1, _, offset1, length1 = parse_header(data1[:HEADER_SIZE])
    assert flags1 == 0
    assert offset1 == 0
    assert length1 == MAX_PIXELS_PER_PACKET

    # Second packet: PUSH, offset=480, length=288
    data2 = sender.sock.sendto.call_args_list[1][0][0]
    _, flags2, _, offset2, length2 = parse_header(data2[:HEADER_SIZE])
    assert flags2 == FLAG_PUSH
    assert offset2 == 480
    assert length2 == 288


def test_send_clear():
    """send_clear sends a CLEAR command packet."""
    sender = FrameSender("127.0.0.1", 21324)
    sender.sock = MagicMock()
    sender.send_clear()

    sender.sock.sendto.assert_called_once()
    data = sender.sock.sendto.call_args[0][0]
    assert data[0] == 0x05  # CMD_CLEAR
