"""Tests for multi-strip indexer."""

from picow_ws2812.indexer import Indexer


def _single_strip():
    return [{"nrows": 8, "ncols": 32, "y_offset": 0, "zigzag": True}]


def _triple_strip():
    return [
        {"nrows": 8, "ncols": 32, "y_offset": 0, "zigzag": True},
        {"nrows": 8, "ncols": 32, "y_offset": 8, "zigzag": True},
        {"nrows": 8, "ncols": 32, "y_offset": 16, "zigzag": True},
    ]


def test_single_strip_total_leds():
    idx = Indexer(_single_strip())
    assert idx.num_leds == 256


def test_triple_strip_total_leds():
    idx = Indexer(_triple_strip())
    assert idx.num_leds == 768


def test_single_strip_origin():
    """Pixel (0,0) maps to index 0."""
    idx = Indexer(_single_strip())
    assert idx.get_pixel_number(0, 0) == 0


def test_single_strip_zigzag():
    """Even column goes top-to-bottom, odd column goes bottom-to-top."""
    idx = Indexer(_single_strip())
    # Even column (x=0): y increases index
    assert idx.get_pixel_number(0, 0) == 0
    assert idx.get_pixel_number(0, 7) == 7
    # Odd column (x=1): y is reversed
    assert idx.get_pixel_number(1, 0) == 15  # 1*8 + (8-1-0)
    assert idx.get_pixel_number(1, 7) == 8  # 1*8 + (8-1-7)


def test_triple_strip_second_panel():
    """Pixels on second strip have offset of 256."""
    idx = Indexer(_triple_strip())
    # (0, 8) is the top-left of the second strip
    assert idx.get_pixel_number(0, 8) == 256


def test_triple_strip_third_panel():
    """Pixels on third strip have offset of 512."""
    idx = Indexer(_triple_strip())
    assert idx.get_pixel_number(0, 16) == 512


def test_out_of_bounds_returns_negative():
    """Out-of-bounds coordinates return -1."""
    idx = Indexer(_single_strip())
    assert idx.get_pixel_number(-1, 0) == -1
    assert idx.get_pixel_number(0, -1) == -1
    assert idx.get_pixel_number(32, 0) == -1
    assert idx.get_pixel_number(0, 8) == -1


def test_no_zigzag():
    """With zigzag=False, all columns go in the same direction."""
    strips = [{"nrows": 8, "ncols": 4, "y_offset": 0, "zigzag": False}]
    idx = Indexer(strips)
    # Both even and odd columns should go top-to-bottom
    assert idx.get_pixel_number(1, 0) == 8  # 1*8 + 0
    assert idx.get_pixel_number(1, 7) == 15  # 1*8 + 7
