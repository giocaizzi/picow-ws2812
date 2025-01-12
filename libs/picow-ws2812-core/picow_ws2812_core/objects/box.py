from typing import Tuple
from ..base import BaseObject, Pixel


class Box(BaseObject):

    def __init__(self, x0: int, y0: int, x1: int, y1: int, color: Tuple[int, int, int]):
        super().__init__()
        self._create_pixels(x0, y0, x1, y1, color)

    def _create_pixels(
        self, x0: int, y0: int, x1: int, y1: int, color: Tuple[int, int, int]
    ):
        # create a line connecting the corners
        for x in range(x0, x1 + 1):
            self.add_pixel(Pixel(x, y0, color))
            self.add_pixel(Pixel(x, y1, color))

        for y in range(y0 + 1, y1):
            self.add_pixel(Pixel(x0, y, color))
            self.add_pixel(Pixel(x1, y, color))
