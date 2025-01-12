"""visualizer module."""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union

from picow_ws2812_core.base import BaseObject, Collection
from picow_ws2812_core import Sequence, View
from picow_ws2812_core.objects.char import Char


class LedWallVisualizer:
    def __init__(self, nrows: int, ncols: int):
        """Initialize the LED wall simulator.

        Args:
            nrows (int): Number of rows.
            ncols (int): Number of columns.
            grid (np.ndarray): Grid of pixels.
        """
        self.nrows = nrows
        self.ncols = ncols

    def render_view(self, view: View):
        """Render a view."""
        fig, ax = plt.subplots()
        ax.imshow(view.get_grid())    

