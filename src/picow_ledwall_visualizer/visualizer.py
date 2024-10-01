"""visualizer module."""

import matplotlib.pyplot as plt
import numpy as np


class LedWallVisualizer:
    def __init__(self, nrows: int, ncols: int):
        """Initialize the LED wall simulator.

        Args:
            nrows (int): Number of rows.
            ncols (int): Number of columns.
        """
        self.nrows = nrows
        self.ncols = ncols
        self.grid = np.zeros((nrows, ncols, 3), dtype=int)

    def fill_grid(self, objects=[]):
        for obj in objects:
            # text
            for char in obj.chars:
                for pixel in char.pixels:
                    x, y, color_tuple = pixel.x, pixel.y, pixel.color
                    self.grid[y, x] = color_tuple

    def show(self):
        """Display the LED wall."""
        # create Array-like object from x, y, color
        plt.imshow(self.grid)
        plt.show()

    def clear(self):
        """Clear the LED wall."""
        self.grid.fill(0)
