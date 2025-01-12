"""visualizer module."""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union

from picow_ws2812_core.base import BaseObject, Collection
from picow_ws2812_core.objects.char import Char


class LedWallVisualizer:
    def __init__(self, nrows: int, ncols: int):
        """Initialize the LED wall simulator.

        Args:
            nrows (int): Number of rows.
            ncols (int): Number of columns.
            grid (np.ndarray): Grid of pixels.
            objects (List[Text]): List of Text objects.
            fig (plt.Figure): Matplotlib figure.
            ax (plt.Axes): Matplotlib axes.
        """
        self.nrows = nrows
        self.ncols = ncols
        self.grid = np.zeros((nrows, ncols, 3), dtype=int)
        self.objects: List[Union[BaseObject, Collection]] = []
        self.fig, self.ax = plt.subplots()
        # quickfix in notebooks init shows the figure (?!?)
        plt.close()

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
            self.render_object(obj)

    def render_object(self, obj):
        """Render a single object or collection of objects."""
        if issubclass(type(obj), (Collection,)):
            for subobj in obj.objects:
                self.render_object(subobj)
        elif issubclass(type(obj), (BaseObject,)):
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
        self.ax.imshow(self.grid)
        if autoclear:
            self._clear_grid()
        return self.fig

    def _clear_grid(self):
        """Clear the LED wall."""
        self.grid.fill(0)
