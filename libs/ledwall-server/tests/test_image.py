"""Tests for image plugins."""

from unittest.mock import MagicMock, patch

import numpy as np
from PIL import Image

from ledwall_server.plugins.image import AnimatedGif, StaticImage


def test_static_image_no_path():
    """StaticImage with no path should render black."""
    plugin = StaticImage({}, 16, 8)
    frame = plugin.render()
    assert frame.shape == (8, 16, 3)
    assert np.all(frame == 0)


def test_static_image_renders_file():
    """StaticImage should render an image file scaled to display size."""
    img = Image.new("RGB", (64, 48), (255, 0, 0))
    with patch.object(Image, "open", return_value=img):
        plugin = StaticImage({"path": "test.png"}, 16, 8)
    frame = plugin.render()
    assert frame.shape == (8, 16, 3)
    assert np.all(frame[:, :, 0] == 255)


def test_static_image_tick_is_noop():
    """StaticImage tick should not change the frame."""
    plugin = StaticImage({}, 16, 8)
    frame1 = plugin.render().copy()
    plugin.tick()
    frame2 = plugin.render()
    assert np.array_equal(frame1, frame2)


def test_animated_gif_no_path():
    """AnimatedGif with no path should render black."""
    plugin = AnimatedGif({}, 16, 8)
    frame = plugin.render()
    assert frame.shape == (8, 16, 3)
    assert np.all(frame == 0)


def test_animated_gif_cycles_frames():
    """AnimatedGif should cycle through frames on tick."""
    # Create a mock GIF with 2 frames
    img = MagicMock(spec=Image.Image)
    frame1 = Image.new("RGB", (16, 8), (255, 0, 0))
    frame2 = Image.new("RGB", (16, 8), (0, 255, 0))
    call_count = 0

    def mock_convert(mode):
        nonlocal call_count
        result = frame1 if call_count == 0 else frame2
        call_count += 1
        return result

    img.convert = mock_convert

    seek_count = 0

    def mock_seek(pos):
        nonlocal seek_count
        seek_count += 1
        if seek_count >= 2:
            raise EOFError
        return None

    img.seek = mock_seek
    img.tell = MagicMock(side_effect=[0, 1])

    with patch.object(Image, "open", return_value=img):
        plugin = AnimatedGif({"path": "test.gif"}, 16, 8)

    assert len(plugin._frames) == 2
    f1 = plugin.render().copy()
    plugin.tick()
    f2 = plugin.render()
    assert not np.array_equal(f1, f2)
