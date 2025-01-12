"""visualizer module."""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union

from picow_ws2812_core.base import Object, ComplexObject


class LedWallVisualizer:
    def __init__(self, nrows: int, ncols: int):
        """Initialize the LED wall simulator.

        Args:
            nrows (int): Number of rows.
            ncols (int): Number of columns.
            grid (np.ndarray): Grid of pixels.
            objects (List[Text]): List of Text objects.
        """
        self.nrows = nrows
        self.ncols = ncols
        self.grid = np.zeros((nrows, ncols, 3), dtype=int)
        self.objects: List[Union[Object, ComplexObject]] = []

    def add_object(self, obj):
        """Add a Text object to the LED wall."""
        self.objects.append(obj)

    def clear(self):
        """Clear all Text objects from the LED wall."""
        self.objects = []
        self._clear_grid()

    def _render(self):
        """Render the Text objects on the grid (led wall)."""
        for obj in self.objects:
            # these objects can be of two types: Object or ComplexObject
            if hasattr(obj, "objects"):
                # ComplexObject
                for subobj in obj.objects:
                    for pixel in subobj.pixels:
                        x, y, color_tuple = pixel.x, pixel.y, pixel.color
                        if 0 <= y < self.nrows and 0 <= x < self.ncols:
                            self.grid[y, x] = color_tuple
            elif hasattr(obj, "pixels"):
                # Object
                for pixel in obj.pixels:
                    x, y, color_tuple = pixel.x, pixel.y, pixel.color
                    if 0 <= y < self.nrows and 0 <= x < self.ncols:
                        self.grid[y, x] = color_tuple
            else:
                raise ValueError(f"Invalid object type {type(obj)}")

    def show(self, autoclear=True):
        """Display the LED wall."""
        # create Array-like object from x, y, color
        self._render()
        plt.imshow(self.grid)
        plt.show()
        if autoclear:
            self._clear_grid()

    def _clear_grid(self):
        """Clear the LED wall."""
        self.grid.fill(0)
