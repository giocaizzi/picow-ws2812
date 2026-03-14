"""CLI entry point for previewing LED wall plugins."""

from __future__ import annotations

import argparse
import sys

from ledwall_server.plugins.clock import Clock
from ledwall_server.plugins.effect import ColorCycle, Rainbow, SolidColor
from ledwall_server.plugins.text import ScrollingText, StaticText
from picow_ws2812_devtools.visualizer import LedWallVisualizer

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
        default="/tmp/ledwall_preview.png",
        help="Output path (default: /tmp/ledwall_preview.png)",
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

    # Auto-switch extension for default output path
    if (
        args.gif
        and not args.output.endswith(".gif")
        and args.output == "/tmp/ledwall_preview.png"
    ):
        args.output = "/tmp/ledwall_preview.gif"

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
