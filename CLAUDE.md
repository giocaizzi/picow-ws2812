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
    /picow-ws2812-devtools :
        Development tools for WS2812 driver
    /picow-ws2812 :
        Core micropython
- main.py : Application entry point
- pyproject.toml : Root project configuration
```   