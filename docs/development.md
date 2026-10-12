# Development

Host-side tooling is managed with [uv](https://docs.astral.sh/uv/). The repo is a uv workspace: the root project is virtual (not packaged) and `libs/*` are its members, installed editable.

| Library | Runs on | Notes |
|---|---|---|
| `libs/picow-ws2812-core` | host + Pico W | Pure-Python objects, collections and fonts; has tests. |
| `libs/picow-ws2812-driver` | Pico W | Imports `machine`/`rp2`; not importable on the host. |
| `libs/picow-ws2812-devtools` | host | matplotlib visualizer used by `notebooks/`. |

## Setup

```sh
uv sync            # creates .venv with all libs and the dev + test groups
uv run pre-commit install
```

## Checks

```sh
make check         # = make lint (ruff check + ruff format --check) + make test (pytest)
```

CI (`.github/workflows/ci.yml`) runs `make check` in the `check` job, after a gitleaks `secrets` job. No hardware is involved.

## Dependencies

```sh
uv add --group dev <pkg>                       # root dev tooling
uv add --package picow-ws2812-driver <pkg>     # a library's runtime dependency
```

Commit `uv.lock` with every dependency change; CI runs with `UV_LOCKED=1` and fails on a stale lock. Dependabot updates `uv` and GitHub Actions weekly.
