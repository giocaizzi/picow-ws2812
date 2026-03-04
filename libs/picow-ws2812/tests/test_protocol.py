"""Tests for protocol module."""

from picow_ws2812.protocol import (
    CMD_FRAME_DATA,
    CMD_PING,
    FLAG_PUSH,
    HEADER_SIZE,
    build_header,
    parse_header,
)


def test_build_and_parse_header_roundtrip():
    """Build a header then parse it — values must match."""
    header = build_header(CMD_FRAME_DATA, FLAG_PUSH, 5, 480, 288)
    assert len(header) == HEADER_SIZE

    result = parse_header(header)
    assert result is not None
    command, flags, sequence, offset, length = result
    assert command == CMD_FRAME_DATA
    assert flags == FLAG_PUSH
    assert sequence == 5
    assert offset == 480
    assert length == 288


def test_parse_header_too_short():
    """Packets shorter than HEADER_SIZE return None."""
    assert parse_header(b"\x01\x02\x03") is None
    assert parse_header(b"") is None


def test_build_header_no_flags():
    """Header with no flags set."""
    header = build_header(CMD_PING, 0, 0, 0, 0)
    command, flags, sequence, offset, length = parse_header(header)
    assert command == CMD_PING
    assert flags == 0
    assert sequence == 0
    assert offset == 0
    assert length == 0


def test_sequence_wraps():
    """Sequence number uses only lower 4 bits (0-15)."""
    header = build_header(CMD_FRAME_DATA, 0, 15, 0, 100)
    _, _, seq, _, _ = parse_header(header)
    assert seq == 15


def test_large_offset_and_length():
    """Offset and length are uint16 (max 65535)."""
    header = build_header(CMD_FRAME_DATA, 0, 0, 65535, 65535)
    _, _, _, offset, length = parse_header(header)
    assert offset == 65535
    assert length == 65535
