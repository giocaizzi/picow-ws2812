"""CLI entry point for previewing LED wall plugins."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ledwall_server.plugins.clock import Clock
from ledwall_server.plugins.effect import ColorCycle, Rainbow, SolidColor
from ledwall_server.plugins.text import ScrollingText, StaticText
from picow_ws2812_devtools.visualizer import LedWallVisualizer

_PREVIEWS_DIR = Path(__file__).resolve().parents[3] / "previews"

PLUGIN_REGISTRY: dict[str, tuple[type, dict]] = {
    "Rainbow": (Rainbow, {"speed": 3}),
    "ColorCycle": (ColorCycle, {"speed": 5}),
    "SolidColor": (SolidColor, {"color": [255, 0, 0]}),
    "ScrollingText": (ScrollingText, {"text": "LED WALL", "color": [0, 200, 255]}),
    "StaticText": (StaticText, {"text": "HELLO", "color": [255, 255, 255]}),
    "Clock": (Clock, {"color": [0, 255, 0]}),
}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Preview LED wall plugins")
    parser.add_argument(
        "plugin",
        choices=sorted(PLUGIN_REGISTRY),
        help="Plugin to preview",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output path (default: backend/previews/<plugin>.png or .gif)",
    )
    parser.add_argument("--width", "-W", type=int, default=32, help="LED width")
    parser.add_argument("--height", "-H", type=int, default=8, help="LED height")
    parser.add_argument("--gif", action="store_true", help="Save as animated GIF")
    parser.add_argument(
        "--frames", "-n", type=int, default=60, help="Number of frames (GIF only)"
    )
    parser.add_argument(
        "--interval", type=int, default=33, help="Frame interval ms (GIF only)"
    )

    args = parser.parse_args(argv)

    if args.output is None:
        ext = ".gif" if args.gif else ".png"
        _PREVIEWS_DIR.mkdir(exist_ok=True)
        args.output = str(_PREVIEWS_DIR / f"{args.plugin}{ext}")

    plugin_cls, default_config = PLUGIN_REGISTRY[args.plugin]
    plugin = plugin_cls(default_config, args.width, args.height)
    viz = LedWallVisualizer(width=args.width, height=args.height)

    if args.gif:
        viz.save_animation(
            args.output,
            plugin=plugin,
            frames=args.frames,
            interval=args.interval,
            title=args.plugin,
        )
    else:
        viz.save_snapshot(args.output, plugin=plugin, title=args.plugin)

    print(f"Saved to {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
