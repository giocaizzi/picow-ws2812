"""Reference sheet generators — full-page catalog of icons, fonts, and elements."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle, Rectangle

from ledwall_server.plugins.elements import (
    BarElement,
    IconElement,
    RectElement,
    TextElement,
)
from ledwall_server.plugins.fonts import measure_text, render_text
from ledwall_server.plugins.icons import ICONS_L, ICONS_S, IconSize
from ledwall_server.plugins.screen import Screen

_ICON_COLORS = {
    "sun": (255, 200, 0),
    "cloud": (180, 180, 180),
    "cloud_sun": (200, 180, 50),
    "rain": (100, 150, 255),
    "snow": (200, 220, 255),
    "storm": (255, 255, 100),
    "drop": (0, 150, 255),
    "wind": (150, 200, 200),
    "thermometer": (255, 80, 80),
    "bitcoin": (247, 147, 26),
    "arrow_up": (0, 255, 0),
    "arrow_down": (255, 0, 0),
}


def _render_bitmap(
    ax: plt.Axes, bitmap: list[str], color: tuple, radius: float
) -> None:
    """Render a bitmap icon as LED dots on an axes."""
    h = len(bitmap)
    w = len(bitmap[0]) if bitmap else 0
    patches = []
    colors = []
    for y, row in enumerate(bitmap):
        for x, ch in enumerate(row):
            patches.append(Circle((x + 0.5, y + 0.5), radius))
            if ch == "1":
                colors.append([c / 255 for c in color] + [1.0])
            else:
                colors.append([0.1, 0.1, 0.1, 0.3])
    coll = PatchCollection(patches, match_original=False)
    coll.set_facecolor(colors)
    coll.set_edgecolor("none")
    ax.add_collection(coll)
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.set_aspect("equal")
    ax.set_facecolor("black")
    ax.axis("off")


def _render_frame_dots(ax: plt.Axes, frame: np.ndarray, radius: float = 0.35) -> None:
    """Render a numpy frame as LED dots on an axes."""
    h, w = frame.shape[:2]
    patches = []
    colors = []
    for y in range(h):
        for x in range(w):
            patches.append(Circle((x + 0.5, y + 0.5), radius))
            r, g, b = frame[y, x]
            if r > 0 or g > 0 or b > 0:
                colors.append([r / 255, g / 255, b / 255, 1.0])
            else:
                colors.append([0.1, 0.1, 0.1, 0.3])
    coll = PatchCollection(patches, match_original=False)
    coll.set_facecolor(colors)
    coll.set_edgecolor("none")
    ax.add_collection(coll)
    ax.add_patch(Rectangle((0, 0), w, h, lw=0.5, ec=(0.25, 0.25, 0.25), fc="none"))
    ax.set_xlim(-0.2, w + 0.2)
    ax.set_ylim(h + 0.2, -0.2)
    ax.set_aspect("equal")
    ax.set_facecolor("black")
    ax.axis("off")


def generate_icons_sheet(out_dir: Path) -> None:
    """Generate a reference sheet for all icons, rendered inside 8x8 canvases."""
    icon_names = list(ICONS_L.keys())
    ncols = 6
    nrows = (len(icon_names) + ncols - 1) // ncols
    canvas_size = 8

    for label, _icons, icon_size in [
        ("Icons — L (7x7 in 8x8)", ICONS_L, IconSize.L),
        ("Icons — S (5x5 in 8x8)", ICONS_S, IconSize.S),
    ]:
        fig, axes = plt.subplots(
            nrows,
            ncols,
            figsize=(3 * ncols, 3 * nrows),
            gridspec_kw={"hspace": 0.5, "wspace": 0.3},
        )
        fig.set_facecolor("black")
        axes = axes.flatten()

        for i, name in enumerate(icon_names):
            color = _ICON_COLORS.get(name, (255, 255, 255))
            canvas = np.zeros((canvas_size, canvas_size, 3), dtype=np.uint8)
            elem = IconElement(
                0,
                0,
                canvas_size,
                canvas_size,
                icon=name,
                color=color,
                icon_size=icon_size,
            )
            elem.draw(canvas)
            _render_frame_dots(axes[i], canvas, radius=0.35)
            axes[i].set_title(name, fontsize=10, color="white", pad=8)

        for i in range(len(icon_names), len(axes)):
            axes[i].set_facecolor("black")
            axes[i].axis("off")

        fig.suptitle(label, fontsize=14, fontweight="bold", color="white", y=0.98)
        suffix = "L" if icon_size == IconSize.L else "S"
        path = out_dir / f"icons_{suffix}.png"
        fig.savefig(str(path), facecolor="black", bbox_inches="tight", dpi=150)
        plt.close(fig)
        print(f"  png: {path.name}", file=sys.stderr)


def generate_fonts_sheet(out_dir: Path) -> None:
    """Generate per-size font reference sheets with full character sets."""
    rows = [
        ("UPPERCASE", "ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
        ("lowercase", "abcdefghijklmnopqrstuvwxyz"),
        ("Digits", "0123456789"),
        ("Symbols", "!@#$%^&*()-_=+[]{}|;:',.<>?/~`\"\\"),
        ("Currency/Units", "$+-.:°"),
    ]
    sizes = [6, 7, 8, 10, 12]
    color = (255, 255, 255)

    for size in sizes:
        nrows = len(rows)
        fig, axes = plt.subplots(
            nrows,
            1,
            figsize=(14, 2.2 * nrows),
            gridspec_kw={"hspace": 0.7},
        )
        fig.set_facecolor("black")

        for i, (label, chars) in enumerate(rows):
            tw, th = measure_text(chars, font_size=size)
            canvas_w = tw + 4
            canvas_h = th + 4
            frame = render_text(chars, canvas_w, canvas_h, color, x=2, font_size=size)
            _render_frame_dots(axes[i], frame, radius=0.35)
            axes[i].set_title(
                f"{label}  ({tw}x{th} px)",
                fontsize=10,
                color="white",
                pad=8,
            )

        fig.suptitle(
            f"Font size {size}",
            fontsize=14,
            fontweight="bold",
            color="white",
            y=0.98,
        )
        path = out_dir / f"font_{size}.png"
        fig.savefig(str(path), facecolor="black", bbox_inches="tight", dpi=150)
        plt.close(fig)
        print(f"  png: {path.name}", file=sys.stderr)


def generate_elements_sheet(out_dir: Path) -> None:
    """Generate a reference sheet showing all element types in 32x8 canvases."""
    # All demos use a consistent 32x8 canvas for scale comparison
    w, h = 32, 8
    demos: list[tuple[str, list]] = [
        (
            "TextElement",
            [
                TextElement(0, 0, w, h, text="Hello", color=(255, 255, 255)),
            ],
        ),
        (
            "TextElement (colored)",
            [
                TextElement(0, 0, w, h, text="LED", color=(0, 200, 255)),
            ],
        ),
        (
            "IconElement L + S",
            [
                IconElement(
                    0, 0, 8, 8, icon="sun", color=(255, 200, 0), icon_size=IconSize.L
                ),
                IconElement(
                    9,
                    1,
                    6,
                    6,
                    icon="bitcoin",
                    color=(247, 147, 26),
                    icon_size=IconSize.S,
                ),
            ],
        ),
        (
            "RectElement (filled)",
            [
                RectElement(0, 0, 16, h, color=(255, 0, 0), fill=True),
            ],
        ),
        (
            "RectElement (outline)",
            [
                RectElement(0, 0, 16, h, color=(0, 255, 0), fill=False),
            ],
        ),
        (
            "BarElement (65% / 30%)",
            [
                BarElement(0, 0, w, 3, value=0.65, color=(0, 200, 0), bg=(30, 30, 30)),
                BarElement(
                    0, 4, w, 3, value=0.30, color=(255, 100, 0), bg=(30, 30, 30)
                ),
            ],
        ),
        (
            "Composed",
            [
                RectElement(0, 0, w, h, color=(20, 20, 20)),
                IconElement(0, 0, 8, 8, icon="sun", color=(255, 200, 0)),
                TextElement(9, 0, 14, h, text="22°", color=(255, 255, 255)),
                BarElement(0, 7, w, 1, value=0.65, color=(0, 200, 0), bg=(50, 50, 50)),
            ],
        ),
    ]

    ncols = 2
    nrows = (len(demos) + ncols - 1) // ncols
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(14, 3 * nrows),
        gridspec_kw={"hspace": 0.6, "wspace": 0.3},
    )
    fig.set_facecolor("black")
    axes = axes.flatten()

    for i, (title, elements) in enumerate(demos):
        screen = Screen(title, elements)
        frame = screen.render(w, h)
        _render_frame_dots(axes[i], frame, radius=0.35)
        axes[i].set_title(title, fontsize=10, color="white", pad=8)

    for i in range(len(demos), len(axes)):
        axes[i].set_facecolor("black")
        axes[i].axis("off")

    fig.suptitle(
        "Elements Reference", fontsize=14, fontweight="bold", color="white", y=0.98
    )
    path = out_dir / "elements.png"
    fig.savefig(str(path), facecolor="black", bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  png: {path.name}", file=sys.stderr)


def generate_all(out_dir: Path) -> None:
    """Generate all reference sheets."""
    out_dir.mkdir(parents=True, exist_ok=True)
    print("[reference/icons]", file=sys.stderr)
    generate_icons_sheet(out_dir)
    print("[reference/fonts]", file=sys.stderr)
    generate_fonts_sheet(out_dir)
    print("[reference/elements]", file=sys.stderr)
    generate_elements_sheet(out_dir)
