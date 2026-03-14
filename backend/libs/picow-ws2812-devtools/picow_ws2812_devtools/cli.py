"""CLI entry point for previewing LED wall plugins and scenes."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ledwall_server.plugins.bitcoin import Bitcoin
from ledwall_server.plugins.clock import Clock
from ledwall_server.plugins.effect import ColorCycle, Rainbow, SolidColor
from ledwall_server.plugins.text import ScrollingText, StaticText
from ledwall_server.plugins.weather import Weather
from ledwall_server.renderer import Renderer
from picow_ws2812_devtools.reference import generate_all as generate_reference
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


def _make_bitcoin(width: int, height: int) -> Bitcoin:
    btc = Bitcoin({"screen_mode": "auto", "screen_interval": 60}, width, height)
    btc._price = 97200.0
    btc._trends = {"24h": 2.3, "48h": -1.5, "7d": 5.2, "1m": 12.1}
    btc._fetched = True
    btc.screen_manager.screens = btc._build_screens()
    return btc


def _make_weather(width: int, height: int) -> Weather:
    weather = Weather({"screen_mode": "auto", "screen_interval": 60}, width, height)
    weather._temp = "22"
    weather._humidity = "65"
    weather._weather_code = 0
    weather._fetched = True
    weather.screen_manager.screens = weather._build_screens()
    return weather


DATA_PLUGIN_REGISTRY: dict[str, type] = {
    "Bitcoin": _make_bitcoin,
    "Weather": _make_weather,
}

SCENE_REGISTRY: dict[str, dict] = {
    "Dashboard": {
        "width": 32,
        "height": 16,
        "dot_radius": 0.3,
        "layers": lambda: [
            (
                _make_weather.__wrapped__(16, 8)
                if hasattr(_make_weather, "__wrapped__")
                else _make_weather(16, 8),
                0,
                0,
            ),
            (_make_bitcoin(16, 8), 16, 0),
            (Clock({"color": [0, 255, 0]}, 16, 8), 0, 8),
            (StaticText({"text": "DASH", "color": [255, 200, 0]}, 16, 8), 16, 8),
        ],
    },
    "Dashboard-Animated": {
        "width": 32,
        "height": 16,
        "dot_radius": 0.3,
        "layers": lambda: [
            (_make_weather(16, 8), 0, 0),
            (_make_bitcoin(16, 8), 16, 0),
            (Clock({"color": [0, 255, 0]}, 16, 8), 0, 8),
            (
                ScrollingText({"text": "LED WALL", "color": [255, 200, 0]}, 16, 8),
                16,
                8,
            ),
        ],
    },
}


def _save(path: Path, msg: str) -> None:
    print(f"  {msg}: {path.name}", file=sys.stderr)


def _export_plugin(
    name: str,
    out_dir: Path,
    width: int,
    height: int,
    gif: bool,
    frames: int,
    interval: int,
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    viz = LedWallVisualizer(width=width, height=height)

    if name in PLUGIN_REGISTRY:
        plugin_cls, default_config = PLUGIN_REGISTRY[name]
        plugin = plugin_cls(default_config, width, height)
    elif name in DATA_PLUGIN_REGISTRY:
        plugin = DATA_PLUGIN_REGISTRY[name](width, height)
    else:
        print(f"Unknown plugin: {name}", file=sys.stderr)
        sys.exit(1)

    viz.save_snapshot(str(out_dir / f"{name}.png"), plugin=plugin, title=name)
    _save(out_dir / f"{name}.png", "png")

    if gif:
        viz.save_animation(
            str(out_dir / f"{name}.gif"),
            plugin=plugin,
            frames=frames,
            interval=interval,
            title=name,
        )
        _save(out_dir / f"{name}.gif", "gif")


def _export_scene(
    name: str,
    out_dir: Path,
    gif: bool,
    frames: int,
    interval: int,
) -> None:
    if name not in SCENE_REGISTRY:
        print(f"Unknown scene: {name}", file=sys.stderr)
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)
    spec = SCENE_REGISTRY[name]
    w, h = spec["width"], spec["height"]
    viz = LedWallVisualizer(width=w, height=h, dot_radius=spec.get("dot_radius", 0.4))
    renderer = Renderer(w, h)
    layers = spec["layers"]()

    viz.save_snapshot(
        str(out_dir / f"{name}.png"), renderer=renderer, layers=layers, title=name
    )
    _save(out_dir / f"{name}.png", "png")

    if gif:
        viz.save_animation(
            str(out_dir / f"{name}.gif"),
            renderer=renderer,
            layers=layers,
            frames=frames,
            interval=interval,
            title=name,
        )
        _save(out_dir / f"{name}.gif", "gif")


def main(argv: list[str] | None = None) -> None:
    all_plugins = sorted(set(PLUGIN_REGISTRY) | set(DATA_PLUGIN_REGISTRY))
    all_scenes = sorted(SCENE_REGISTRY)
    all_names = all_plugins + all_scenes

    parser = argparse.ArgumentParser(description="Preview LED wall plugins and scenes")
    parser.add_argument(
        "target",
        nargs="?",
        default="all",
        choices=all_names + ["all", "reference"],
        help="Plugin/scene/reference name, or 'all' (default: all)",
    )
    parser.add_argument("--width", "-W", type=int, default=32, help="LED width")
    parser.add_argument("--height", "-H", type=int, default=8, help="LED height")
    parser.add_argument("--gif", action="store_true", help="Also save animated GIFs")
    parser.add_argument(
        "--frames", "-n", type=int, default=120, help="Number of frames (GIF)"
    )
    parser.add_argument(
        "--interval", type=int, default=33, help="Frame interval ms (GIF)"
    )

    args = parser.parse_args(argv)

    if args.target == "reference":
        generate_reference(_PREVIEWS_DIR / "reference")
        return

    if args.target == "all":
        targets = all_names
        args.gif = True
        generate_reference(_PREVIEWS_DIR / "reference")
    else:
        targets = [args.target]

    for name in targets:
        print(f"[{name}]", file=sys.stderr)
        if name in PLUGIN_REGISTRY or name in DATA_PLUGIN_REGISTRY:
            _export_plugin(
                name,
                _PREVIEWS_DIR / "plugins",
                args.width,
                args.height,
                args.gif,
                args.frames,
                args.interval,
            )
        elif name in SCENE_REGISTRY:
            _export_scene(
                name,
                _PREVIEWS_DIR / "scenes",
                args.gif,
                args.frames,
                args.interval,
            )


if __name__ == "__main__":
    main()
