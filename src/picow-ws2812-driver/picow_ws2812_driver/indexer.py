"""indexer module."""


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