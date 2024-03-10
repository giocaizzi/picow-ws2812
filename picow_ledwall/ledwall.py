from picow_ledwall.neopixel import Neopixel


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

    def display(self, obj):
        """display pixels on the led wall"""
        for pixel, color in obj.pixels:
            for x, y in pixel:
                self.set_pixel(self.indexer.get_pixel_number(x, y), color)
        self.show()

    def clear_all(self):
        self.clear()
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
