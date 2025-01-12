"""base classes."""

from typing import List, Tuple
from abc import ABC, abstractmethod


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

    def __repr__(self) -> str:
        """Return string representation of pixel."""
        return self.__str__()

    def __str__(self) -> str:
        """Return string representation of pixel."""
        return f"Pixel({self.x}, {self.y}, {self.color})"


class Object(ABC):
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

    @abstractmethod
    def _create_pixels(self) -> None:
        """Create pixels for the object."""
        pass

    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        """Return bounding box of object.

        Returns:
            Tuple[int, int, int, int]: x0, y0, x1, y1
        """
        x0 = min([pixel.x for pixel in self.pixels])
        y0 = min([pixel.y for pixel in self.pixels])
        x1 = max([pixel.x for pixel in self.pixels])
        y1 = max([pixel.y for pixel in self.pixels])
        return x0, y0, x1, y1

    def __repr__(self) -> str:
        """Return string representation of object."""
        return self.__str__()

    def __str__(self) -> str:
        """Return string representation of object."""
        return f"{self.__class__.__name__}(bbox={self.bbox})"


class ComplexObject(ABC):
    """Base class for complex objects.

    A complex object is a collection of objects that
    function as a single object."""

    objects: List[Object] = []

    def __init__(self):
        """Create a ComplexObject object."""
        self.objects = []

    def add_object(self, obj: Object) -> None:
        """Add an object to the complex object.

        Args:
            obj (Object): object
        """
        self.objects.append(obj)

    @abstractmethod
    def _create_objects(self) -> None:
        """Create objects for the complex object."""
        pass

    @property
    def bbox(self) -> Tuple[int, int, int, int]:
        """Return bounding box of complex object.

        Returns:
            Tuple[int, int, int, int]: x0, y0, x1, y1
        """
        x0 = min([obj.bbox[0] for obj in self.objects])
        y0 = min([obj.bbox[1] for obj in self.objects])
        x1 = max([obj.bbox[2] for obj in self.objects])
        y1 = max([obj.bbox[3] for obj in self.objects])
        return x0, y0, x1, y1

    def move(self, dx: int, dy: int) -> None:
        """Move complex object."""
        for obj in self.objects:
            obj.move(dx, dy)

    def __repr__(self) -> str:
        """Return string representation of complex object."""
        return self.__str__()
    
    def __str__(self) -> str:
        """Return string representation of complex object."""
        return f"{self.__class__.__name__}(bbox={self.bbox})"
