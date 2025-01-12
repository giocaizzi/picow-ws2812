"""visualizer module."""

import matplotlib.pyplot as plt
from picow_ws2812_core import Sequence, View


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

    def render_sequence(self, sequence: Sequence):
        """Render a sequence."""
        fig, ax = plt.subplots()
        for view in sequence.views:
            self.render_view(view)
            plt.pause(1)
