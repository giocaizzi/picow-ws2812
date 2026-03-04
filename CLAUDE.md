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

### Backend

Python server and micropython code for the Pico W. 

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

### 3D models

OpenSCAD files for the ledwall enclosure and mounting brackets.


## Setup specs:

- Raspberry Pi Pico W
- 5x 8x32 ws2812 strips stacked vertically (total 40x32)
- 5V 10A power supply