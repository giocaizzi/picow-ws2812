"""ledwall module"""

import time

from picow_ws2812_driver.indexer import Indexer
from picow_ws2812_driver.neopixel import Neopixel
from picow_ws2812_core.base import View, Sequence


class LedWall(Neopixel):
    _default_brightness = 1
    wait = 1.0

    def __init__(self, nrows: int, ncols: int, GPIO_PIN: int):
        """initialize the led wall

        Args:
            nrows (int): number of rows
            ncols (int): number of columns
            GPIO_PIN (int): GPIO pin number
        """
        try:
            # create the neopixel object
            super().__init__(nrows * ncols, 0, GPIO_PIN, mode="RGB")
            # create the indexer
            self.indexer = Indexer(nrows, ncols, row_height=7)
        except Exception as e:
            raise e

        # set the default brightness
        self.brightness(self._default_brightness)

    def display(self, sequence: Sequence):
        """display sequence on the led wall

        Args:
            sequence (Sequence): sequence to display
        """
        for view in sequence.views:
            self._show_view(view=view)

    def _show_view(self, view: View):
        """display object on the led wall

        Args:
            obj (object): object to display, object must have a
                `pixels` attribute
            wait (int, optional): time to wait before clearing the display.
                Defaults to 1.
        """
        for obj in view.objects:
            for pixel, color in obj.pixels:
                for x, y in pixel:
                    try:
                        self.set_pixel(self.indexer.get_pixel_number(x, y), color)
                    # ignore out of range pixels
                    except IndexError:
                        pass
                    except Exception as e:
                        raise e
        self.show()
        time.sleep(self.wait)
        self.clear()
