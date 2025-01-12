from picow_ws2812_core.base import BaseObject, Collection


from typing import List, Optional


class Group(Collection):
    """Group of objects.

    A Group object is a collection of objects.
    """

    def __init__(self, objects: Optional[List[BaseObject]] = None):
        """Create a Group object."""
        super().__init__()
        if objects:
            for obj in objects:
                self.add_object(obj)

    def _create_objects(self) -> None:
        """Create objects for the group."""
        pass