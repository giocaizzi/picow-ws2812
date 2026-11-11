# AGENTS.md

MicroPython driver for a WS2812B LED wall on a Raspberry Pi Pico W, a host-side frame server, devtools and the 3D-printed enclosure. Development setup and layout: [docs/development.md](docs/development.md).

## Commands

- `make check` before every PR (lint + test). `make help` lists targets.
- Python tooling is `uv` only; never pip or poetry.

## Gotchas

- `libs/picow-ws2812` is MicroPython-only: never add CPython-only code to it. `neopixel`, `ledwall`, `receiver`, `wifi`, `fallback` and `main.py` import MicroPython modules (`machine`, `rp2`, `network`, `uasyncio`); they cannot be imported or tested on the host.
- `neopixel.py` is PIO assembly and is excluded from ruff lint; `libs/picow-ws2812/picow_ws2812/fonts.py` is excluded from ruff entirely.
- Keep `3d/dimensions.txt` in step with `3d/ledwall_enclosure.scad`.
- Preview plugins without hardware: `uv run preview <name>` ([docs/development.md](docs/development.md#previews)).

## Workflow

- `main` changes only via squash-merged PRs with a Conventional Commit title; the required CI check is `check`.
- Repo-wide conventions: [giocaizzi GitHub standard](https://github.com/giocaizzi/.github/blob/main/docs/standard.md).
