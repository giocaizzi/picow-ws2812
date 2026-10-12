# AGENTS.md

MicroPython driver for a WS2812B LED wall on a Raspberry Pi Pico W, plus host-side tooling. Development setup and layout: [docs/development.md](docs/development.md).

## Commands

- `make check` before every PR (lint + test). `make help` lists targets.
- Python tooling is `uv` only; never pip or poetry.

## Gotchas

- `picow_ws2812_driver` and `main.py` import MicroPython modules (`machine`, `rp2`); they cannot be imported or tested on the host.
- `neopixel.py` is PIO assembly and is excluded from ruff lint; `fonts.py` is excluded from ruff entirely.
- `libs/picow-ws2812-core/tests/test_text.py` is a strict xfail until #19 is fixed.

## Workflow

- `main` changes only via squash-merged PRs with a Conventional Commit title; the required CI check is `check`.
- Repo-wide conventions: [giocaizzi GitHub standard](https://github.com/giocaizzi/.github/blob/main/docs/standard.md).
