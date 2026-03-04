"""Indexer module for mapping 2D coordinates to linear pixel indices.

Supports multi-strip configurations where multiple LED panels
are stacked vertically and daisy-chained on a single GPIO pin.
"""


class Indexer:
    """Map global (x, y) coordinates to linear pixel indices across strips.

    The linear pixel space is contiguous: strip0 occupies indices 0..N0-1,
    strip1 occupies N0..N0+N1-1, etc. Each strip has its own zigzag logic.
    """

    def __init__(self, strips):
        """Create an Indexer for one or more LED strips.

        Args:
            strips: list of dicts, each with keys:
                - nrows (int): number of rows in this strip
                - ncols (int): number of columns in this strip
                - y_offset (int): global y position of strip's top row
                - zigzag (bool): whether columns alternate direction
        """
        self.strips = strips
        # Pre-compute the linear offset for each strip
        self._offsets = []
        offset = 0
        for strip in strips:
            self._offsets.append(offset)
            offset += strip["nrows"] * strip["ncols"]
        self.num_leds = offset

    def get_pixel_number(self, x, y):
        """Map global (x, y) to linear pixel index.

        Returns the linear index or -1 if the coordinate is out of bounds.
        """
        for i, strip in enumerate(self.strips):
            y_off = strip["y_offset"]
            nrows = strip["nrows"]
            ncols = strip["ncols"]
            local_y = y - y_off
            if 0 <= local_y < nrows and 0 <= x < ncols:
                if strip.get("zigzag", True) and x % 2 == 1:
                    return self._offsets[i] + x * nrows + (nrows - 1 - local_y)
                else:
                    return self._offsets[i] + x * nrows + local_y
        return -1
