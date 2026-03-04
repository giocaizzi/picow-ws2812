# Project Context

Developing a Micropython-based ledwall controller using WS2812 LEDs on Raspberry Pi Pico W. The project includes:
- Core WS2812 functionality (text, effects, shapes)
- High-level WS2812 driver with effects (indexer, ledwall, neopixel abstrations)
- Development tools for WS2812 driver (Visualization)

# Rules

The `picow-s2812` package is **Micropython-only**. Do not include any Python code that is not compatible with Micropython.


---

# Quick Reference

## Project structure:

```
-/libs
    /picow-ws2812 :
        Core MicroPython library (neopixel, indexer, ledwall, protocol, receiver, wifi, fallback)
    /picow-ws2812-devtools :
        Development tools for WS2812 driver (matplotlib visualizer)
    /ledwall-server :
        Pi5 FastAPI server (renderer, sender, plugins, scene manager, REST API)
- main.py : Pico W asyncio entry point
- pyproject.toml : Root uv workspace configuration
```   

---

# Notebooks

The [notebooks](./notebooks) contain notebooks used to preview the WS2812 effects and animations. Keep it up to date.