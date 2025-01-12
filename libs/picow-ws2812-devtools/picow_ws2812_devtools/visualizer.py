"""visualizer module."""

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from picow_ws2812_core import StaticSequence, StaticView

#


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

    def render_view(self, view: StaticView):
        """Render a view."""
        fig, ax = plt.subplots()
        self._render_grid(ax, view.get_grid())

    def _render_grid(self, ax, grid):
        """Render a grid."""
        ax.imshow(grid)

    def render_sequence(self, sequence: StaticSequence, interval: int = 500):
        """Render a sequence."""
        fig, ax = plt.subplots()
        frames = sequence.get_frames()
        im = ax.imshow(frames[0])

        def update(frame):
            im.set_data(frame)
            return im,  # Return a list containing the im object

        ani = FuncAnimation(fig, update, frames=frames, blit=True, interval=interval)

        plt.show()

        return ani
