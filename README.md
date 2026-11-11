<div align="center">

# picow-ws2812

**MicroPython driver for a WS2812B LED wall on a Raspberry Pi Pico W.**

[![CI](https://github.com/giocaizzi/picow-ws2812/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/giocaizzi/picow-ws2812/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

A MicroPython package to power a WS2812B LED wall matrix, a host-side server that renders and streams frames to it, preview tooling and a 3D-printed enclosure.

## Quickstart

```sh
uv sync
make check
```

## Features

- `libs/picow-ws2812`: PIO-based driver, objects and fonts, and a UDP frame receiver for the Pico W
- `libs/ledwall-server`: FastAPI server that renders plugins and scenes and streams frames to the wall
- `libs/picow-ws2812-devtools`: visualizer and `preview` CLI for plugins and scenes
- `3d/`: OpenSCAD enclosure and dimensions reference

## Documentation

Setup, layout and checks: [docs/development.md](docs/development.md).

## License

[MIT](LICENSE)
