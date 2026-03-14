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
    """Generate a reference sheet for all icons in both sizes."""
    icon_names = list(ICONS_L.keys())
    ncols = 4
    nrows = (len(icon_names) + ncols - 1) // ncols

    for label, icons, _icon_px, radius in [
        ("Icons — L (7x7)", ICONS_L, 7, 0.4),
        ("Icons — S (5x5)", ICONS_S, 5, 0.35),
    ]:
        fig, axes = plt.subplots(
            nrows,
            ncols,
            figsize=(10, 2.5 * nrows),
            gridspec_kw={"hspace": 0.5, "wspace": 0.3},
        )
        fig.set_facecolor("black")
        axes = axes.flatten()

        for i, name in enumerate(icon_names):
            color = _ICON_COLORS.get(name, (255, 255, 255))
            _render_bitmap(axes[i], icons[name], color, radius)
            axes[i].set_title(name, fontsize=10, color="white", pad=8)

        for i in range(len(icon_names), len(axes)):
            axes[i].set_facecolor("black")
            axes[i].axis("off")

        fig.suptitle(label, fontsize=14, fontweight="bold", color="white", y=0.98)
        suffix = label.split("—")[1].strip().split()[0]
        path = out_dir / f"icons_{suffix}.png"
        fig.savefig(str(path), facecolor="black", bbox_inches="tight", dpi=150)
        plt.close(fig)
        print(f"  png: {path.name}", file=sys.stderr)


def generate_fonts_sheet(out_dir: Path) -> None:
    """Generate a reference sheet showing text at different font sizes."""
    sample = "AaBb0123!@#"
    sizes = [6, 7, 8, 10, 12, 14]
    colors = [
        (255, 255, 255),
        (0, 200, 255),
        (255, 200, 0),
        (0, 255, 100),
        (255, 100, 100),
        (200, 150, 255),
    ]

    fig, axes = plt.subplots(
        len(sizes),
        1,
        figsize=(12, 2 * len(sizes)),
        gridspec_kw={"hspace": 0.6},
    )
    fig.set_facecolor("black")

    for i, (size, color) in enumerate(zip(sizes, colors, strict=True)):
        tw, th = measure_text(sample, font_size=size)
        # Add padding
        canvas_w = tw + 4
        canvas_h = th + 4
        frame = render_text(sample, canvas_w, canvas_h, color, x=2, font_size=size)
        _render_frame_dots(axes[i], frame, radius=0.35)
        axes[i].set_title(
            f"Font size {size}  ({tw}x{th} px)",
            fontsize=10,
            color="white",
            pad=8,
        )

    fig.suptitle(
        "Font Reference", fontsize=14, fontweight="bold", color="white", y=0.98
    )
    path = out_dir / "fonts.png"
    fig.savefig(str(path), facecolor="black", bbox_inches="tight", dpi=150)
    plt.close(fig)
    print(f"  png: {path.name}", file=sys.stderr)


def generate_elements_sheet(out_dir: Path) -> None:
    """Generate a reference sheet showing all element types."""
    demos: list[tuple[str, int, int, list]] = [
        (
            "TextElement",
            24,
            8,
            [
                TextElement(0, 0, 24, 8, text="Hello", color=(255, 255, 255)),
            ],
        ),
        (
            "TextElement (colored)",
            24,
            8,
            [
                TextElement(0, 0, 24, 8, text="LED", color=(0, 200, 255)),
            ],
        ),
        (
            "IconElement — L",
            8,
            8,
            [
                IconElement(
                    0, 0, 8, 8, icon="sun", color=(255, 200, 0), icon_size=IconSize.L
                ),
            ],
        ),
        (
            "IconElement — S",
            6,
            6,
            [
                IconElement(
                    0,
                    0,
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
            12,
            8,
            [
                RectElement(0, 0, 12, 8, color=(255, 0, 0), fill=True),
            ],
        ),
        (
            "RectElement (outline)",
            12,
            8,
            [
                RectElement(0, 0, 12, 8, color=(0, 255, 0), fill=False),
            ],
        ),
        (
            "BarElement (65%)",
            24,
            3,
            [
                BarElement(0, 0, 24, 3, value=0.65, color=(0, 200, 0), bg=(30, 30, 30)),
            ],
        ),
        (
            "BarElement (30%)",
            24,
            3,
            [
                BarElement(
                    0, 0, 24, 3, value=0.30, color=(255, 100, 0), bg=(30, 30, 30)
                ),
            ],
        ),
        (
            "Composed",
            32,
            8,
            [
                RectElement(0, 0, 32, 8, color=(20, 20, 20)),
                IconElement(0, 0, 8, 8, icon="sun", color=(255, 200, 0)),
                TextElement(9, 0, 14, 8, text="22°", color=(255, 255, 255)),
                BarElement(0, 7, 32, 1, value=0.65, color=(0, 200, 0), bg=(50, 50, 50)),
            ],
        ),
    ]

    ncols = 3
    nrows = (len(demos) + ncols - 1) // ncols
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(14, 3.5 * nrows),
        gridspec_kw={"hspace": 0.6, "wspace": 0.3},
    )
    fig.set_facecolor("black")
    axes = axes.flatten()

    for i, (title, w, h, elements) in enumerate(demos):
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
