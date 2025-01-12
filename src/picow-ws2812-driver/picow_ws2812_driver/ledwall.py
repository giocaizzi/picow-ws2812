"""ledwall module"""

import time

from picow_ws2812_driver.indexer import Indexer
from picow_ws2812_driver.neopixel import Neopixel
from picow_ws2812_driver.text import TextString


class LedWall(Neopixel):
    _default_brightness = 1

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
        # show welcome message
        self.display(TextString("Hello!", color=(0, 255, 0)), wait=2)

    def display(self, obj, wait: float = 1.0):
        """display object on the led wall

        Args:
            obj (object): object to display, object must have a
                `pixels` attribute
            wait (int, optional): time to wait before clearing the display.
                Defaults to 1.
        """
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
        time.sleep(wait)
        self.clear()

    def quit(self):
        """clear the display and release the GPIO"""
        self.clear()
        self.show()
        # show the goodbye message
        self.display(TextString("Bye", color=(0, 0, 255)), wait=0.5)
        self.display(TextString("Bye Bye!", color=(0, 255, 0)), wait=0.5)
        # show the clear display
        self.show()
