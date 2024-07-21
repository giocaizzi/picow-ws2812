"""ledwall module"""

import time

from picow_ledwall.neopixel import Neopixel
from picow_ledwall.text import TextString


class LedWall(Neopixel):
    _default_brightness = 1

    def __init__(self, nrows, ncols, GPIO_PIN):
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


class Indexer:
    def __init__(self, nrows, ncols, row_height):
        self.nrows = nrows
        self.ncols = ncols
        self.n = nrows * ncols
        self.row_height = row_height

    def get_pixel_number(self, x, y):
        """get linar pixel number from x, y coordinates"""
        # NOTE:
        # the nativE pixel indexing starts at 0
        # and zigzags from the input side (see back of the LED panel)
        # to the output side
        if x % 2 == 0:
            return x * self.nrows + y
        else:
            return x * self.nrows + (self.nrows - 1 - y)
