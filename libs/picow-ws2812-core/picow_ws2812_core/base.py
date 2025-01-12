"""base classes."""

from typing import List, Tuple


CHAR_WIDTH = 5
CHAR_HEIGHT = 7


class Pixel:
    """Pixel object.

    A Pixel object is a representation of a single pixel
    in the ledwall.

    Attributes:
        x (int): x position
        y (int): y position
        color (Tuple[int, int, int]): color
    """

    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        """Create a Pixel object.

        Create a Pixel object with an x and y position and a color.

        Args:
            x (int): x position
            y (int): y position
            color (Tuple[int, int, int]): color
        """
        self._x = x
        self._y = y
        self._color = color

    @property
    def x(self) -> int:
        """Return x position of pixel."""
        return self._x

    @x.setter
    def x(self, x: int):
        """Set x position of pixel.

        Args:
            x (int): x position
        """
        self._x = x

    @property
    def y(self) -> int:
        """Return y position of pixel."""
        return self._y

    @y.setter
    def y(self, y: int):
        """Set y position of pixel.

        Args:
            y (int): y position
        """
        self._y = y

    @property
    def color(self) -> Tuple[int, int, int]:
        """Return color of pixel."""
        return self._color

    @color.setter
    def color(self, color: Tuple[int, int, int]):
        """Set color of pixel.

        Args:
            color (Tuple[int, int, int]): color
        """
        self._color = color

    def move(self, dx: int, dy: int) -> None:
        """Move pixel."""
        self.x += dx
        self.y += dy


class Object:
    """Base class for all objects displayed on the ledwall.

    Attributes:
        pixels (List[Pixel]): list of pixels
    """

    pixels: List[Pixel] = []

    def __init__(self):
        """Create an Object object."""
        self.pixels = []

    def add_pixel(self, pixel: Pixel) -> None:
        """Add a pixel to the object.

        Args:
            pixel (Pixel): pixel
        """
        self.pixels.append(pixel)

    def move(self, dx: int, dy: int) -> None:
        """Move object."""
        for pixel in self.pixels:
            pixel.move(dx, dy)
