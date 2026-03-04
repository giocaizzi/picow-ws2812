"""LedWall module — thin wrapper over Neopixel + Indexer."""

from picow_ws2812.indexer import Indexer
from picow_ws2812.neopixel import Neopixel


class LedWall(Neopixel):
    """LED wall controller combining Neopixel driver with multi-strip Indexer."""

    def __init__(self, strips_config, gpio_pin, state_machine=0, mode="GRB"):
        """Initialize the LED wall.

        Args:
            strips_config: list of strip dicts for Indexer
                (each with nrows, ncols, y_offset, zigzag)
            gpio_pin: GPIO pin number for WS2812 data line
            state_machine: PIO state machine id (default 0)
            mode: color mode string (default "GRB")
        """
        self.indexer = Indexer(strips_config)
        total_leds = self.indexer.num_leds
        super().__init__(total_leds, state_machine, gpio_pin, mode=mode)

        self.nrows = sum(s["nrows"] for s in strips_config)
        self.ncols = strips_config[0]["ncols"]
        self.brightness(1)

    def set_pixel_xy(self, x, y, color):
        """Set pixel by 2D coordinate.

        Args:
            x: column index
            y: row index
            color: (r, g, b) tuple
        """
        idx = self.indexer.get_pixel_number(x, y)
        if idx >= 0:
            self.set_pixel(idx, color)
