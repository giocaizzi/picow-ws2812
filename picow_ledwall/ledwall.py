from picow_ledwall.neopixel import Neopixel

class LedWall(Neopixel):
    _default_brightness = 1

    def __init__(self, nrows, ncols, GPIO_PIN):
        self.nrows = nrows
        self.ncols = ncols
        self.numpix = nrows * ncols
        # create the neopixel object
        super().__init__(self.numpix, 0, GPIO_PIN, mode="RGB")
        self.brightness(self._default_brightness)

    def get_pixel_number(self, x, y):
        """get linar pixel number from x, y coordinates"""
        if x % 2 == 0:
            return x * self.nrows + y
        else:
            return x * self.nrows + (self.nrows - 1 - y)

    def exit(self):
        self.clear()
        self.show()