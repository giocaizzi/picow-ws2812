---
paths:
  - "backend/**"
description: "Instructions for the backend component of the picow-ws2812 project. Use this when working with the backend codebase, such as the micropython code for the Pico W and the Python server."
---

## Previews

Use the CLI to preview LED wall plugins:

```sh
uv run preview Rainbow              # PNG snapshot → backend/previews/Rainbow.png
uv run preview Rainbow --gif -n 60  # GIF animation → backend/previews/Rainbow.gif
```

The `backend/previews/` directory is gitignored.
