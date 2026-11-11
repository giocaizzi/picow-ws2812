# Development

Host-side tooling is managed with [uv](https://docs.astral.sh/uv/). The repo is a uv workspace: the root project is virtual (not packaged) and `libs/*` are its members, installed editable.

| Path | Runs on | Notes |
|---|---|---|
| `libs/picow-ws2812` | Pico W | MicroPython library: neopixel PIO driver, indexer, ledwall, UDP frame protocol, receiver, WiFi, fallback mode; `core` holds the objects, collections and fonts. MicroPython-only: no CPython-only code. The pure-Python parts are tested on the host. |
| `libs/ledwall-server` | host (e.g. a Raspberry Pi 5) | FastAPI server: renderer, plugins (clock, text, weather, bitcoin, images, effects), scene manager, UDP frame sender, REST API. |
| `libs/picow-ws2812-devtools` | host | matplotlib visualizer, `preview` CLI and reference sheets. |
| `main.py` | Pico W | asyncio entry point: WiFi, UDP frame receiver, fallback mode. |
| `3d/` | - | OpenSCAD enclosure (`ledwall_enclosure.scad`) and the component dimensions reference (`dimensions.txt`; keep it up to date). |
| `docs/diagrams/` | - | Wiring diagram (HTML). |

Hardware: Raspberry Pi Pico W, 8x32 WS2812B panels stacked vertically with data on GP28, 5 V 10 A supply. The panel layout is `STRIPS_CONFIG` in `main.py`.

## Setup

```sh
uv sync            # creates .venv with all libs and the dev + test groups
uv run pre-commit install
```

## Checks

```sh
make check         # = make lint (ruff check + ruff format --check + mypy) + make test (pytest)
```

CI (`.github/workflows/ci.yml`) runs `make check` in the `check` job, after a gitleaks `secrets` job. No hardware is involved.

## Previews

Render plugins and scenes on the host, without hardware:

```sh
uv run preview ScrollingText              # PNG -> previews/plugins/
uv run preview ScrollingText --gif -n 60  # also an animated GIF
uv run preview reference                  # icon, font and element sheets -> previews/reference/
uv run preview                            # everything
```

`uv run preview --help` lists the plugins and scenes. `previews/` is gitignored.

## Dependencies

```sh
uv add --group dev <pkg>                  # root dev tooling
uv add --package ledwall-server <pkg>     # a library's runtime dependency
```

Commit `uv.lock` with every dependency change; CI runs with `UV_LOCKED=1` and fails on a stale lock. Dependabot updates `uv` and GitHub Actions weekly.
