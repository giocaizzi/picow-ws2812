<div align="center">

# picow-ws2812

**MicroPython driver for a WS2812B LED wall on a Raspberry Pi Pico W.**

[![CI](https://github.com/giocaizzi/picow-ws2812/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/giocaizzi/picow-ws2812/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

A simple MicroPython package to power a WS2812B LED wall matrix, with host-side tooling to preview it.

## Quickstart

```sh
uv sync
make check
```

## Features

- `libs/picow-ws2812-driver`: PIO-based driver for the Pico W
- `libs/picow-ws2812-core`: pure-Python objects, collections and fonts, tested on the host
- `libs/picow-ws2812-devtools`: matplotlib visualizer used by the notebooks

## Documentation

Setup, layout and checks: [docs/development.md](docs/development.md).

## License

[MIT](LICENSE)
