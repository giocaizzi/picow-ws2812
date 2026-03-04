"""Tests for server-side protocol module."""

from ledwall_server.protocol import (
    CMD_FRAME_DATA,
    CMD_PING,
    FLAG_PUSH,
    HEADER_SIZE,
    build_header,
    parse_header,
)


def test_build_and_parse_roundtrip():
    header = build_header(CMD_FRAME_DATA, FLAG_PUSH, 7, 480, 288)
    assert len(header) == HEADER_SIZE
    command, flags, seq, offset, length = parse_header(header)
    assert command == CMD_FRAME_DATA
    assert flags == FLAG_PUSH
    assert seq == 7
    assert offset == 480
    assert length == 288


def test_parse_too_short():
    assert parse_header(b"\x01") is None


def test_ping_header():
    header = build_header(CMD_PING, 0, 0, 0, 0)
    command, flags, seq, offset, length = parse_header(header)
    assert command == CMD_PING
    assert flags == 0
