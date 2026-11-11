"""Tests for icon bitmap definitions."""

import pytest

from ledwall_server.plugins.icons import ICONS_L, ICONS_S, IconSize, get_icon

EXPECTED_ICONS = [
    "sun",
    "cloud",
    "cloud_sun",
    "rain",
    "snow",
    "storm",
    "drop",
    "wind",
    "thermometer",
    "bitcoin",
    "arrow_up",
    "arrow_down",
]


class TestIconSets:
    """Both icon sets must have all expected icons with correct dimensions."""

    @pytest.mark.parametrize("name", EXPECTED_ICONS)
    def test_icons_s_dimensions(self, name: str) -> None:
        bitmap = ICONS_S[name]
        assert len(bitmap) == 5, f"{name}: expected 5 rows, got {len(bitmap)}"
        for row in bitmap:
            assert len(row) == 5, f"{name}: expected 5 cols, got {len(row)}"

    @pytest.mark.parametrize("name", EXPECTED_ICONS)
    def test_icons_l_dimensions(self, name: str) -> None:
        bitmap = ICONS_L[name]
        assert len(bitmap) == 7, f"{name}: expected 7 rows, got {len(bitmap)}"
        for row in bitmap:
            assert len(row) == 7, f"{name}: expected 7 cols, got {len(row)}"

    @pytest.mark.parametrize("name", EXPECTED_ICONS)
    def test_icons_only_valid_chars(self, name: str) -> None:
        for size_icons in (ICONS_S, ICONS_L):
            for row in size_icons[name]:
                assert set(row) <= {"1", "."}, f"{name}: invalid chars in '{row}'"

    def test_s_and_l_have_same_keys(self) -> None:
        assert set(ICONS_S) == set(ICONS_L)


class TestGetIcon:
    def test_get_icon_default_size(self) -> None:
        assert get_icon("sun") == ICONS_L["sun"]

    def test_get_icon_small(self) -> None:
        assert get_icon("sun", IconSize.S) == ICONS_S["sun"]

    def test_get_icon_missing(self) -> None:
        assert get_icon("nonexistent") is None
